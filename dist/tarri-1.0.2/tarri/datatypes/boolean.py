#==============================================================================#
# File    : boolean.py                                                         #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Definisi tipe data 'boolean' yang digunakan oleh mesin bahasa Tarri.       #
#==============================================================================#

from tarri.datatypes import DATATYPES, register


@register("boolean")
class Boolean:
    def __init__(self, value):
        self.value = bool(value)

    def __str__(self):
        return "benar" if self.value else "salah"
