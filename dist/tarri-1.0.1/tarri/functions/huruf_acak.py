#==============================================================================#
# File    : huruf_acak.py                                                      #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'huruf_acak' yang tersedia dalam bahasa         #
#   Tarri.                                                                     #
#==============================================================================#

import string
import secrets


def huruf_acak(length):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    try:
        length = int(length)
    except ValueError:
        length = 5
    return "".join(secrets.choice(chars) for _ in range(length))
