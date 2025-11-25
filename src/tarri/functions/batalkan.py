# batalkan.py
# Implementasi fungsi batalkan() seperti Laravel abort(),
# lengkap dengan HTML bawaan untuk semua kode error umum.

import subprocess

class BatalkanError(Exception):
    """Exception khusus untuk menangani error batalkan()."""
    def __init__(self, kode, pesan, html):
        self.kode = kode
        self.pesan = pesan
        self.html = html
        super().__init__(pesan)
        
def get_tarri_version():
    try:
        result = subprocess.run(
            ["tarri", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return "[tarriweb | server] Versi tidak ditemukan"

# Template HTML bawaan untuk semua error
def _buat_html_default(kode, pesan):
    return f"""
<html><head><meta charset="utf-8"><title>Error {kode} • TarriWeb</title></head>
    <body style="font-family:sans-serif;text-align:center;margin-top:15%">
        <h1>{kode}</h1><p>{pesan}</p>
        <p style="font-size:12px;color:#777">TarriWeb • {get_tarri_version()}</p>
    </body></html>
"""


# Deskripsi default untuk error HTTP umum
DESKRIPSI_DEFAULT = {
    400: "Permintaan tidak valid.",
    401: "Anda harus login untuk mengakses halaman ini.",
    403: "Anda tidak memiliki akses.",
    404: "Halaman tidak ditemukan.",
    405: "Metode tidak diizinkan.",
    408: "Waktu permintaan habis.",
    409: "Terjadi konflik data.",
    410: "Halaman ini sudah tidak tersedia.",
    422: "Data tidak valid.",
    429: "Terlalu banyak permintaan.",
    500: "Kesalahan server internal.",
    501: "Fitur belum diimplementasikan.",
    502: "Bad Gateway.",
    503: "Layanan tidak tersedia.",
    504: "Gateway timeout."
}


def batalkan(kode, pesan=None):

    # Ambil pesan default jika pesan custom tidak diberikan
    pesan_final = pesan or DESKRIPSI_DEFAULT.get(kode, "Terjadi kesalahan.")

    # Buat HTML bawaan
    html = _buat_html_default(kode, pesan_final)

    # Lempar exception ke server
    raise BatalkanError(kode, pesan_final, html)
