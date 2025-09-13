from tarri.datatypes import register
from tarri.datatypes.desimal import Desimal


@register("angka")
class Angka(int):
    """Tipe data bilangan bulat dalam TARRI"""

    def __new__(cls, value):
        return super().__new__(cls, int(value))

    def __add__(self, other):
        from tarri.datatypes.kata import Kata  # lazy import
        if isinstance(other, (int, float, Angka, Desimal)):
            if isinstance(other, float) or isinstance(other, Desimal):
                return Desimal(float(self) + float(other))
            return Angka(int(self) + int(other))
        if isinstance(other, Kata):
            return Kata(str(self) + str(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan tipe ini")

    def __sub__(self, other):
        if isinstance(other, (int, float, Angka, Desimal)):
            if isinstance(other, float) or isinstance(other, Desimal):
                return Desimal(float(self) - float(other))
            return Angka(int(self) - int(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan tipe ini")

    def __mul__(self, other):
        from tarri.datatypes.kata import Kata  # lazy import
        if isinstance(other, (int, float, Angka, Desimal)):
            if isinstance(other, float) or isinstance(other, Desimal):
                return Desimal(float(self) * float(other))
            return Angka(int(self) * int(other))
        if isinstance(other, Kata):  # angka × kata → ulangi string
            return Kata(str(other) * int(self))
        raise TypeError("[tarri] angka tidak bisa diproses dengan tipe ini")

    def __truediv__(self, other):
        if isinstance(other, (int, float, Angka, Desimal)):
            return Desimal(float(self) / float(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan tipe ini")

    def __mod__(self, other):
        if isinstance(other, (int, float, Angka)):
            return Angka(int(self) % int(other))
        raise TypeError("[tarri] angka tidak bisa diproses dengan tipe ini")

    def __repr__(self):
        return str(int(self))

    def __str__(self):
        return str(int(self))
