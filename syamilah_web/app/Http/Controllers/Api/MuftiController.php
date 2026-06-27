<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MuftiController extends Controller
{
    public function tanya(Request $request)
    {
        // 1. Validasi input
        $request->validate([
            'pertanyaan' => 'required|string'
        ]);

        $pertanyaan = $request->input('pertanyaan');

        // Di Docker: http://python-api:8001 (via .env), di lokal: http://127.0.0.1:8001
        $muftiApiUrl = config('services.mufti.api_url');

        try {
            // 2. Tembak API Python FastAPI (Pastikan server Python menyala)
            $response = Http::timeout(60)->post($muftiApiUrl . '/tanya-mufti', [
                'pertanyaan' => $pertanyaan
            ]);

            // 3. Kembalikan respons ke pengguna
            if ($response->successful()) {
                return response()->json($response->json());
            }

            return response()->json([
                'status' => 'error',
                'message' => 'Gagal mendapatkan jawaban dari Mesin AI.'
            ], 500);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Koneksi ke server AI terputus: ' . $e->getMessage()
            ], 500);
        }
    }
}
