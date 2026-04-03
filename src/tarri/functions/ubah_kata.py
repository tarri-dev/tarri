#==============================================================================#
# File    : ubah_kata.py                                                       #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'ubah_kata' yang tersedia dalam bahasa          #
#   Tarri.                                                                     #
#==============================================================================#

def ubah_kata(x):
    """
    Mengubah apapun menjadi string dengan aman.

    - None → ""
    - List/Dict → representasi JSON
    - Semua tipe lain → str()
    """
    import json

    if x is None:
        return ""
    elif isinstance(x, (list, dict)):
        try:
            return json.dumps(x, ensure_ascii=False)
        except Exception:
            return str(x)
    else:
        return str(x)
