import os
import re
import sys

# Aturan Regex untuk mencari print() atau debugPrint()
REGEX_PATTERN = r"(print|debugPrint)\s*\((.*?)\)"

# Kata kunci data pribadi (PII) yang dicari di dalam fungsi log
PII_KEYWORDS = ["id", "email", "name", "token", "password"]

def jalankan_pemindaian(direktori_target):
    jumlah_pelanggaran = 0
    
    # Berjalan menyusuri folder 'lib' secara otomatis
    for folder_saat_ini, _, daftar_berkas in os.walk(direktori_target):
        for nama_berkas in daftar_berkas:
            # Hanya memeriksa berkas yang berakhiran .dart
            if nama_berkas.endswith('.dart'):
                jalur_berkas = os.path.join(folder_saat_ini, nama_berkas)
                
                # Buka dan baca isi berkas Dart baris demi baris
                with open(jalur_berkas, 'r', encoding='utf-8') as berkas:
                    for nomor_baris, isi_baris in enumerate(berkas, 1):
                        
                        # Cek apakah ada fungsi print atau debugPrint
                        pencocokan = re.search(REGEX_PATTERN, isi_baris)
                        if pencocokan:
                            # Ambil teks yang ada di dalam tanda kurung fungsi log
                            isi_argumen = pencocokan.group(2).lower()
                            
                            # Cek apakah teks tersebut mengandung kata kunci PII
                            for kata_kunci in PII_KEYWORDS:
                                if kata_kunci in isi_argumen:
                                    print(f"[BAHAYA PRIVASI] Berkas: {jalur_berkas} | Baris: {nomor_baris}")
                                    print(f"  Kode Bermasalah: {isi_baris.strip()}\n")
                                    jumlah_pelanggaran += 1
                                    break # Keluar dari perulangan kata kunci, lanjut baris berikutnya
                                    
    return jumlah_pelanggaran

if __name__ == "__main__":
    folder_lib = "./lib"
    
    if not os.path.exists(folder_lib):
        print("Folder ./lib tidak ditemukan. Pastikan dijalankan di root proyek Flutter.")
        sys.exit(0)
        
    print("--- MEMULAI PEMINDAIAN PRIVASI (LIGHTWEIGHT SAST) ---")
    total_bocor = jalankan_pemindaian(folder_lib)
    print("-----------------------------------------------------")
    
    # Logika exit-code untuk gerbang otomatisasi (Quality Gate)
    if total_bocor > 0:
        print(f"Hasil: Pemindaian GAGAL. Ditemukan {total_bocor} kebocoran data pribadi!")
        sys.exit(1) # Status 1 menandakan ada error (menghentikan GitHub Actions)
    else:
        print("Hasil: Pemindaian SUKSES. Kode Anda bersih dari bocoran PII pada log.")
        sys.exit(0) # Status 0 menandakan aman (GitHub Actions lolos)