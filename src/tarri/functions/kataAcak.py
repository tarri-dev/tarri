import random
import string

def kataAcak(length):
    """Menghasilkan string acak sepanjang length"""
    try:
        length = int(length)
    except ValueError:
        length = 5  # default jika bukan angka
    return ''.join(random.choices(string.ascii_lowercase, k=length))


# CARA MENGGUNAKAN FUNGSI kataAcak()

# titikawal{
#     _nama = kataAcak(27)
#     cetak _nama
#     }