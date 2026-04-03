#==============================================================================#
# File    : tipe_data.py                                                       #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'tipe_data' yang tersedia dalam bahasa          #
#   Tarri.                                                                     #
#==============================================================================#

def tipe_data(val):
    """Mengembalikan nama tipe data dalam bahasa Indonesia"""
    # Urutan penting, agar tidak salah deteksi
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, int):
        return "angka"
    elif isinstance(val, float):
        return "desimal"
    elif isinstance(val, str):
        return "kata"
    elif isinstance(val, list):
        return "daftar"
    elif isinstance(val, dict):
        return "objek"
    elif isinstance(val, tuple):
        return "kumpulan"
    elif isinstance(val, set):
        return "himpuan"
    elif val is None:
        return "kosong"
    else:
        return "tidak diketahui"
