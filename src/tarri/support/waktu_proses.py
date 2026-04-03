#==============================================================================#
# File    : waktu_proses.py                                                    #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Fungsi dan utilitas pendukung 'waktu_proses' yang membantu operasi         #
#   inti Tarri.                                                                #
#==============================================================================#

# tarri/src/tarri/support/waktu_proses.py
import time


def waktu_proses():
    """
    Fungsi global TARRI, menghitung waktu proses kode TARRI dari awal
    hingga akhir tag <tarri>.
    """
    mulai = time.time()

    # jalankan semua kode TARRI di tag saat ini
    # ... tergantung implementasi interpreter
    # contoh dummy:
    # interpreter.run_current_tag()

    selesai = time.time()
    return round(selesai - mulai, 4)
