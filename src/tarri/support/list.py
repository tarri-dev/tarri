# 📚 Modul Array/List untuk Tarri
from typing import Any, List

def unik(daftar: List[Any]) -> List[Any]:
    """
    Menghapus duplikat dari daftar, mempertahankan urutan asli.
    """
    hasil = []
    terlihat = set()
    for item in daftar:
        if item not in terlihat:
            hasil.append(item)
            terlihat.add(item)
    return hasil


def cari_index(daftar: List[Any], value: Any) -> int:
    """
    Mencari posisi value dalam daftar.
    Jika tidak ditemukan, mengembalikan -1.
    """
    try:
        return daftar.index(value)
    except ValueError:
        return -1


def hapus_index(daftar: List[Any], index: int) -> List[Any]:
    """
    Menghapus elemen dari daftar berdasarkan index.
    Mengembalikan daftar baru tanpa mengubah daftar asli.
    """
    if 0 <= index < len(daftar):
        return daftar[:index] + daftar[index+1:]
    return daftar.copy()  # index di luar jangkauan, kembalikan salinan


def balik(daftar: List[Any]) -> List[Any]:
    """
    Membalik urutan elemen dalam daftar.
    """
    return daftar[::-1]

