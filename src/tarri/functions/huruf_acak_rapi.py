import string
import secrets
import sys

def huruf_acak_rapi(length):
    chars = string.ascii_lowercase + string.digits  # a-z0-9
    
    # Validasi panjang
    if length not in (4, 8, 12, 16):
        print("[LOG ACAK RAPI] Angka yang diterima hanya 4, 8, 12, atau 16.", file=sys.stderr)
        return None

    # Buat string acak sesuai panjang
    raw = ''.join(secrets.choice(chars) for _ in range(length))

    # Bagi setiap 4 huruf
    blok = [raw[i:i+4] for i in range(0, len(raw), 4)]

    # Gabungkan dengan tanda "-"
    return '-'.join(blok)
