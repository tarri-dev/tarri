from tarri.datatypes import DATATYPES, register

@register("boolean")
class Boolean:
    def __init__(self, value):
        self.value = bool(value)

    def __str__(self):
        return "benar" if self.value else "salah"
