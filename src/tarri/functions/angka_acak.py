import random

def angka_acak(min_val=0, max_val=100):
    """
    Menghasilkan angka acak antara min_val dan max_val (inklusif).
    Default: 0-100
    """
    try:
        min_val = int(min_val)
        max_val = int(max_val)
    except ValueError:
        min_val, max_val = 0, 100
    return random.randint(min_val, max_val)


# cara menggunakan funsi angka_acak()

# titikawal{
#     _nilai = angka_acak(10, 100000)
#     cetak _nilai
# }