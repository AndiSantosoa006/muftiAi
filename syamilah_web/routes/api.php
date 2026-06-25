<?php

use App\Http\Controllers\Api\MuftiController;
use Illuminate\Support\Facades\Route;

Route::post('/chat-mufti', [MuftiController::class, 'tanya']);
