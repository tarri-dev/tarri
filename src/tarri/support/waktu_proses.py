# tarri/src/tarri/support/waktu_proses.py
import time

def waktu_proses_tarri():
    """
    Fungsi global TARRI, menghitung waktu proses kode TARRI dari awal
    hingga akhir tag <tarri>.
    """
    # ini akan diisi oleh TARRI Web, misal jalankan interpreter untuk kode yang diukur
    mulai = time.time()

    # jalankan semua kode TARRI di tag saat ini
    # ... tergantung implementasi interpreter
    # contoh dummy:
    # interpreter.run_current_tag()

    selesai = time.time()
    return round(selesai - mulai, 4)
