import string
import secrets


def kata_acak(length):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    try:
        length = int(length)
    except ValueError:
        length = 5
    return ''.join(secrets.choice(chars) for _ in range(length))



# CARA MENGGUNAKAN FUNGSI kataAcak()

# titikawal{
#     _nama = kata_acak(27)
#     cetak _nama
#     }