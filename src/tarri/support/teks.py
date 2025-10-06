def panjang(teks: str) -> int:
    """
    Menghitung panjang string.
    """
    return len(teks)


def besar(teks: str) -> str:
    """
    Mengubah teks menjadi huruf besar semua.
    """
    return str(teks).upper()


def kecil(teks: str) -> str:
    """
    Mengubah teks menjadi huruf kecil semua.
    """
    return str(teks).lower()


def ganti(teks: str, dari: str, ke: str) -> str:
    """
    Mengganti substring 'dari' dengan 'ke' dalam teks.
    """
    return str(teks).replace(dari, ke)


def gabung(list_teks: list, pemisah: str = "") -> str:
    """
    Menggabungkan list string dengan pemisah tertentu.
    Default: tanpa pemisah.
    """
    return str(pemisah).join(map(str, list_teks))

def awal_kapital(teks: str) -> str:
    """Huruf awal tiap kata kapital (capitalize)"""
    return str(teks).title()