from tarri.datatypes import DATATYPES, register

@register("null")
class Null:
    def __init__(self):
        self.value = None

    def __str__(self):
        return "kosong"
