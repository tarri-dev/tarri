#==============================================================================#
# File    : uuid.py                                                            #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'uuid' yang tersedia dalam bahasa Tarri.        #
#==============================================================================#

import uuid


def UUID():
    """
    Menghasilkan UUID versi 4 (acak)
    """
    return str(uuid.uuid4())


# cara menggunakan UUID()
# titikawal{
#     _id = UUID()
#     cetak _id
# }
