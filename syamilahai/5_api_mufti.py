from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
import google.generativeai as genai

app = FastAPI(title="API Maktabah Syamilah AI")

API_KEY = "AIzaSyB9Sndz93NxtyQa3JFSBIDgvWcpc27jEXg" # Pastikan memasukkan API Key yang benar
genai.configure(api_key=API_KEY)

# Konfigurasi Model: Gunakan 1.5-flash untuk performa penalaran terbaik
generation_config = {"temperature": 0.3, "top_p": 0.9, "top_k": 40}
model = genai.GenerativeModel(model_name='gemini-3.1-flash-lite', generation_config=generation_config)

client = chromadb.PersistentClient(path="./referensi")
koleksi_kitab = client.get_collection(name="koleksi_fikih_global")

class InputPertanyaan(BaseModel):
    pertanyaan: str

@app.post("/tanya-mufti")
async def proses_tanya_mufti(input_data: InputPertanyaan):
    try:
        # =====================================================================
        # TAHAP 1: AI AGEN PERTAMA (Ekspansi Kata Kunci Dinamis)
        # =====================================================================
        prompt_kata_kunci = f"""
        Anda adalah ahli Ushul Fiqh tingkat lanjut. Tugas Anda adalah membedah persoalan (takhrij al-manath) dari pertanyaan pengguna sebelum mencari dalilnya di database Kitab Kuning.
        Pertanyaan: "{input_data.pertanyaan}"
        
        Langkah Berpikir (Internal):
        1. Jika pertanyaan adalah masalah kontemporer (misal: paylater, asuransi, dropship), urai menjadi akad dasar fikihnya (misal: jual beli, utang bersyarat, sewa, gadai).
        2. Ekstrak sinonim dan kata kunci dalam bahasa Arab dan Indonesia berdasarkan akar masalah fikih tersebut.
        
        ATURAN MUTLAK:
        1. KEMBALIKAN HANYA KATA KUNCI, dipisahkan dengan koma.
        2. DILARANG MENJAWAB PERTANYAAN. DILARANG MEMBERI PENJELASAN atau teks tambahan apa pun selain kata kunci.
        """
        
        respon_kata_kunci = model.generate_content(prompt_kata_kunci)
        kata_kunci_dinamis = respon_kata_kunci.text.strip()
        
        query_pencarian_final = f"{input_data.pertanyaan}, {kata_kunci_dinamis}"
        print(f"DEBUG - Kata Kunci Pencarian: {query_pencarian_final}")

        # =====================================================================
        # TAHAP 2: PENCARIAN DATABASE (Multi-Referensi)
        # =====================================================================
        hasil_pencarian = koleksi_kitab.query(
            query_texts=[query_pencarian_final],
            n_results=3, 
            include=['documents', 'metadatas', 'distances']
        )

        daftar_referensi_teks = ""
        data_sumber_lengkap = []
        
        if hasil_pencarian['documents'] and hasil_pencarian['documents'][0]:
            for i in range(len(hasil_pencarian['documents'][0])):
                teks = hasil_pencarian['documents'][0][i]
                metadata = hasil_pencarian['metadatas'][0][i]
                
                sumber_kotor = metadata.get('sumber', "Kitab Tidak Diketahui")
                sumber_bersih = sumber_kotor.replace('file ', '').replace('.htm', '').replace('.html', '').strip()
                halaman = metadata.get('halaman', "Tidak Disebutkan")
                jarak = hasil_pencarian['distances'][0][i]
                
                if jarak < 1.5: 
                    daftar_referensi_teks += f"\n[Referensi {i+1} | Sumber: {sumber_bersih} | Halaman: {halaman}]\n{teks}\n"
                    data_sumber_lengkap.append({
                        "teks": teks, 
                        "sumber": sumber_bersih,
                        "halaman": halaman
                    })

        # FALLBACK: Jika referensi lokal kosong, buka akses Pengetahuan Global
        if not daftar_referensi_teks:
            daftar_referensi_teks = "[KOSONG - Tidak ada referensi lokal yang relevan. Gunakan Pengetahuan Global Anda untuk menjawab, dan beri tahu pengguna bahwa jawaban ini di luar database lokal.]"

        # =====================================================================
        # TAHAP 3: AI AGEN KEDUA (Mufti Utama Menganalisis Multi-Referensi)
        # =====================================================================
        prompt_utama = f"""
        Anda adalah Asisten Cendekiawan Muslim dan Pakar Literasi Islam AI yang cerdas, dinamis, dan memiliki wawasan lintas disiplin tingkat dunia.

        Tugas Anda adalah merespons pertanyaan pengguna berdasarkan Kumpulan Referensi Teks Arab dari database. Namun, JIKA REFERENSI KOSONG atau TIDAK RELEVAN, Anda DIPERBOLEHKAN menggunakan Pengetahuan Global Anda.
        
        ATURAN MUTLAK GAYA BAHASA:
        1. DILARANG KERAS menggunakan simbol Markdown seperti pagar (#) atau bintang (*).
        2. Gunakan teks biasa murni dengan penomoran angka biasa (1, 2, 3, 4).

        ATURAN NALAR KOGNITIF (ANALISIS DINAMIS):
        1. SESUAIKAN SUDUT PANDANG: Analisis referensi sesuai isinya (Sanad, Lughah, Tarikh, atau Fikih).
        2. JIKA MENGGUNAKAN REFERENSI LOKAL: Teks Arab WAJIB diberi HARAKAT lengkap. DILARANG memotong teks di tengah kalimat.
        3. JIKA MENGGUNAKAN PENGETAHUAN GLOBAL: Jawab dengan komprehensif layaknya pakar, namun sebutkan secara halus bahwa informasi ini bersumber dari luar database sistem.

        Gunakan persis struktur teks biasa berikut (tanpa simbol Markdown):

        1. Intisari dan Konteks Teks
        Berikan ringkasan langsung atas pertanyaan. Sebutkan apakah ini berdasarkan referensi lokal atau wawasan global.

        2. Teks Arab dan Terjemahan
        Teks Asli: (Jika dari referensi lokal, kutip secara UTUH dengan HARAKAT sempurna. Jika dari global, kutip dalil umum yang relevan).
        Sumber: (Sebutkan nama kitab/sumbernya).
        Terjemahan: (Berikan terjemahan bahasa Indonesia yang akurat).

        3. Analisis Komprehensif
        Bongkar makna teks sesuai disiplin ilmunya. Jika ini masalah kontemporer, jelaskan analoginya (qiyas).

        4. Saran Pertanyaan Lanjutan
        Berikan 1 atau 2 pertanyaan menarik yang relevan agar pengguna bisa mengeksplorasi topik ini lebih jauh.

        =======================================
        KUMPULAN REFERENSI TEKS ARAB DARI DATABASE: 
        {daftar_referensi_teks}

        Pertanyaan Pengguna: "{input_data.pertanyaan}"
        =======================================
        Berikan respons dinamis Anda sekarang:
        """

        respon_utama = model.generate_content(prompt_utama)

        return {
            "status": "sukses",
            "pertanyaan": input_data.pertanyaan,
            "jawaban_ai": respon_utama.text,
            "data_referensi": data_sumber_lengkap 
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))