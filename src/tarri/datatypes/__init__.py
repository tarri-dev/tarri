# tarri/datatypes/__init__.py

# 1️⃣ Definisi register harus di atas
DATATYPES = {}

def register(name):
    """Decorator untuk mendaftarkan tipe data baru"""
    def wrapper(cls):
        DATATYPES[name] = cls
        return cls
    return wrapper

# 2️⃣ Baru import class
from .angka import Angka
from .kata import Kata
from .desimal import Desimal
from .boolean import Boolean
from .null import Null
from .daftar import Daftar
