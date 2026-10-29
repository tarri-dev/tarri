#==============================================================================#
# File    : null.py                                                            #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Definisi tipe data 'null' yang digunakan oleh mesin bahasa Tarri.          #
#==============================================================================#

from tarri.datatypes import DATATYPES, register


@register("null")
class Null:
    def __init__(self):
        self.value = None

    def __str__(self):
        return "kosong"
