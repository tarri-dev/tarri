from tarri.datatypes import DATATYPES, register

@register("daftar")
class Daftar:
    def __init__(self, items=None):
        self.value = items or []

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.value) + "]"
