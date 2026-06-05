import os
import re
import sys
import time  # 1. Tambahkan modul time

# Aturan Regex untuk mencari print() atau debugPrint()
REGEX_PATTERN = r"(print|debugPrint)\s*\((.*?)\)"

# Kata kunci data pribadi (PII)
PII_KEYWORDS = ["id", "email", "name", "token", "password"]

def jalankan_pemindaian(direktori_target):
    jumlah_pelanggaran = 0
    
    for folder_saat_ini, _, daftar_berkas in os.walk(direktori_target):
        for nama_berkas in daftar_berkas:
            if nama_berkas.endswith('.dart'):
                jalur_berkas = os.path.join(folder_saat_ini, nama_berkas)
                
                with open(jalur_berkas, 'r', encoding='utf-8') as berkas:
                    for nomor_baris, isi_baris in enumerate(berkas, 1):
                        pencocokan = re.search(REGEX_PATTERN, isi_baris)
                        if pencocokan:
                            isi_argumen = pencocokan.group(2).lower()
                            for kata_kunci in PII_KEYWORDS:
                                if kata_kunci in isi_argumen:
                                    print(f"[BAHAYA PRIVASI] Berkas: {jalur_berkas} | Baris: {nomor_baris}")
                                    print(f"  Kode Bermasalah: {isi_baris.strip()}\n")
                                    jumlah_pelanggaran += 1
                                    break
                                    
    return jumlah_pelanggaran

if __name__ == "__main__":
    folder_lib = "./lib"
    
    if not os.path.exists(folder_lib):
        print("Folder ./lib tidak ditemukan.")
        sys.exit(0)
        
    print("--- MEMULAI PEMINDAIAN PRIVASI (LIGHTWEIGHT SAST) ---")
    
    # 2. Catat waktu mulai
    waktu_mulai = time.time()
    
    total_bocor = jalankan_pemindaian(folder_lib)
    
    # 3. Catat waktu selesai dan hitung durasi
    waktu_selesai = time.time()
    durasi = waktu_selesai - waktu_mulai
    
    print("-----------------------------------------------------")
    print(f"Waktu pemindaian skrip: {durasi:.4f} detik") # 4. Tampilkan durasi
    print("-----------------------------------------------------")
    
    if total_bocor > 0:
        print(f"Hasil: Pemindaian GAGAL. Ditemukan {total_bocor} kebocoran!")
        sys.exit(1)
    else:
        print("Hasil: Pemindaian SUKSES. Kode Anda bersih.")
        sys.exit(0)