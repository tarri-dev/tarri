"""
Fungsi dasar Tarri versi Bahasa Indonesia.
Berbasis interpreter, tapi tidak semua fungsi butuh akses interpreter.
"""

from typing import Any


def himpunan(interpreter: Any, args: list):
    """
    Membuat himpunan (set) dari iterable.
    Contoh:
        himpunan("aiueoAIUEO") -> {'a','i','u','e','o','A','I','U','E','O'}
    """
    _ = interpreter  # Parameter tidak digunakan, diamkan agar tidak error Pylance
    if not args:
        return set()
    data = args[0]
    try:
        return set(data)
    except Exception:
        return {data}


def jumlah(interpreter: Any, args: list):
    """
    Menjumlahkan seluruh elemen numerik dalam iterable.
    Contoh:
        jumlah([1,2,3]) -> 6
    """
    _ = interpreter
    if not args:
        return 0

    data = args[0]

    if isinstance(data, (list, tuple, set)):
        try:
            return sum(data)
        except TypeError:
            # Jika ada elemen non-numerik, lewati
            return sum(x for x in data if isinstance(x, (int, float)))

    elif isinstance(data, (int, float)):
        return data

    return 0


def semua(interpreter: Any, args: list):
    """
    Mengembalikan True jika semua elemen True.
    Contoh:
        semua([True, True, False]) -> False
    """
    _ = interpreter
    if not args:
        return False
    return all(args[0])


def ada(interpreter: Any, args: list):
    """
    Mengembalikan True jika ada minimal satu elemen True.
    Contoh:
        ada([False, True, False]) -> True
    """
    _ = interpreter
    if not args:
        return False
    return any(args[0])
