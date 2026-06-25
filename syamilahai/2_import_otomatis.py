import chromadb
import uuid
import glob
import time # Tambahan untuk mengukur waktu eksekusi
from bs4 import BeautifulSoup

# 1. Buka database ChromaDB lokal
client = chromadb.PersistentClient(path="./referensi")
koleksi_kitab = client.get_or_create_collection(name="koleksi_fikih_global")

# 2. Cari SEMUA file yang berakhiran .htm di folder saat ini
daftar_file_htm = glob.glob("*.htm")
print(f"Mendeteksi {len(daftar_file_htm)} file HTM yang akan diproses: {daftar_file_htm}\n")

# Konstanta Batch: Berapa paragraf yang diunggah dalam satu kali proses
BATCH_SIZE = 500 

# 3. Looping: Memproses file satu per satu secara otomatis
for nama_file in daftar_file_htm:
    print(f"▶ Memulai proses untuk file: {nama_file}...")
    waktu_mulai = time.time() # Mulai menghitung waktu
    
    # Buka dan baca file
    with open(nama_file, "r", encoding="utf-8") as file:
        html_mentah = file.read()

    # Bersihkan kode HTML menjadi teks murni
    soup = BeautifulSoup(html_mentah, "html.parser")
    teks_bersih = soup.get_text(separator="\n")

    # Potong menjadi paragraf dan buang yang kosong/terlalu pendek
    daftar_paragraf = teks_bersih.split("\n")
    daftar_paragraf_bersih = [p.strip() for p in daftar_paragraf if len(p.strip()) > 50]
    
    total_paragraf = len(daftar_paragraf_bersih)
    print(f"  ↳ Ditemukan {total_paragraf} paragraf valid. Sedang menyimpan (Metode Batch)...")

    # Jika ada isinya, masukkan ke database
    if total_paragraf > 0:
        # Buat ID unik dan metadata sumber untuk tiap paragraf
        daftar_id = [str(uuid.uuid4()) for _ in range(total_paragraf)]
        daftar_sumber = [{"sumber": f"Kitab dari file {nama_file}"} for _ in range(total_paragraf)]

        # --- SISTEM BATCHING (Pemecahan Data) ---
        for i in range(0, total_paragraf, BATCH_SIZE):
            # Ambil potongan data sesuai batch size
            batch_teks = daftar_paragraf_bersih[i : i + BATCH_SIZE]
            batch_id = daftar_id[i : i + BATCH_SIZE]
            batch_sumber = daftar_sumber[i : i + BATCH_SIZE]

            try:
                # Simpan ke ChromaDB secara bertahap
                koleksi_kitab.add(
                    documents=batch_teks,
                    metadatas=batch_sumber,
                    ids=batch_id
                )
                print(f"    ✔ Terunggah: {min(i + BATCH_SIZE, total_paragraf)} / {total_paragraf} paragraf")
            except Exception as e:
                print(f"    ❌ Gagal mengunggah batch pada indeks {i}. Error: {e}")

    waktu_selesai = time.time() - waktu_mulai
    print(f"  ✅ File {nama_file} berhasil dimasukkan ke otak AI dalam {waktu_selesai:.2f} detik!\n")

print("🎉 ALHAMDULILLAH! Seluruh file HTM telah selesai dibersihkan dan disimpan.")