#==============================================================================#
# File    : desimal.py                                                         #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Definisi tipe data 'desimal' yang digunakan oleh mesin bahasa Tarri.       #
#==============================================================================#

from tarri.datatypes import register


@register("desimal")
class Desimal(float):
    """Tipe data bilangan desimal dalam TARRI"""

    def __new__(cls, value):
        return super().__new__(cls, float(value))

    def __add__(self, other):
        if isinstance(other, (int, float, Desimal)):
            return Desimal(float(self) + float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan kata")

    def __sub__(self, other):
        if isinstance(other, (int, float, Desimal)):
            return Desimal(float(self) - float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan kata")

    def __mul__(self, other):
        if isinstance(other, (int, float, Desimal)):
            return Desimal(float(self) * float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan kata")

    def __truediv__(self, other):
        if isinstance(other, (int, float, Desimal)):
            return Desimal(float(self) / float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan kata")

    def __mod__(self, other):
        if isinstance(other, (int, float, Desimal)):
            return Desimal(float(self) % float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan kata")

    def __repr__(self):
        return str(float(self))

    def __str__(self):
        return str(float(self))
