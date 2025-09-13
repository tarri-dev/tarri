from tarri.datatypes import register


@register("kata")
class Kata(str):
    """Tipe data string dalam TARRI"""

    def __new__(cls, value):
        return super().__new__(cls, str(value))

    def __add__(self, other):
        return Kata(super().__add__(str(other)))

    def __mul__(self, other):
        from tarri.datatypes.angka import Angka  # lazy import
        if isinstance(other, (int, Angka)):
            return Kata(super().__mul__(int(other)))
        raise TypeError("[tarri] perkalian kata hanya bisa dengan angka")

    def __repr__(self):
        return super().__str__()

    def __str__(self):
        return super().__str__()
