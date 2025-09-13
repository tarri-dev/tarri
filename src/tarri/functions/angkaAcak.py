import random

def angkaAcak(min_val=0, max_val=100):
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


# cara menggunakan funsi angkaAcak()

# titikawal{
#     _nilai = angkaAcak(10, 100000)
#     cetak _nilai
# }