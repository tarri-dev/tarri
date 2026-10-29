#==============================================================================#
# File    : daftar.py                                                          #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Definisi tipe data 'daftar' yang digunakan oleh mesin bahasa Tarri.        #
#==============================================================================#

from tarri.datatypes import DATATYPES, register


@register("daftar")
class Daftar:
    def __init__(self, items=None):
        self.value = items or []

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.value) + "]"
