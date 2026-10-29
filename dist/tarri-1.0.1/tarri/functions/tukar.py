#==============================================================================#
# File    : tukar.py                                                           #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'tukar' yang tersedia dalam bahasa Tarri.       #
#==============================================================================#

def tukar(data, i, j):
    """
    Tukar elemen pada list 'data' index i dan j.
    Mengembalikan list baru, tidak mengubah list asli.
    """
    if not isinstance(data, list):
        return data

    panjang = len(data)
    if i < 0 or j < 0 or i >= panjang or j >= panjang:
        return data

    # duplikasi list
    baru = data.copy()

    # swap
    temp = baru[i]
    baru[i] = baru[j]
    baru[j] = temp

    return baru
