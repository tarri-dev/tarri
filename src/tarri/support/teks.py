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


def gabung(data, pemisah="") -> str:
    """
    Menggabungkan data apa pun (list, tuple, scalar)
    tetapi string diperlakukan sebagai satu item.
    """

    def flatten(x):
        # String dianggap satu elemen, BUKAN dipecah
        if isinstance(x, str):
            yield x

        # dict → key saja
        elif isinstance(x, dict):
            for k in x.keys():
                yield k

        # iterable lain
        elif isinstance(x, (list, tuple, set)):
            for item in x:
                yield from flatten(item)

        # scalar (int, bool, float, None)
        else:
            yield x

    return str(pemisah).join(str(i) for i in flatten(data))


def awal_kapital(teks: str) -> str:
    """Huruf awal tiap kata kapital (capitalize)"""
    return str(teks).title()

def kunci(data):
    """Mengembalikan daftar kunci dari dict (kamus)"""
    if isinstance(data, dict):
        return list(data.keys())
    raise TypeError("kunci() hanya bisa digunakan untuk tipe kamus (dict)")

def nilai(data):
    """Mengembalikan daftar value dari dict (kamus)"""
    if isinstance(data, dict):
        return list(data.values())
    raise TypeError("nilai() hanya bisa digunakan untuk tipe kamus (dict)")

