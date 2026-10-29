#==============================================================================#
# File    : list.py                                                            #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Fungsi dan utilitas pendukung 'list' yang membantu operasi inti Tarri.     #
#==============================================================================#

# 📚 Modul Array/List untuk Tarri
from typing import Any, List


def tambah(daftar: List[Any], item: Any):
    """
    Menambahkan item ke akhir daftar.
    """
    daftar.append(item)
    return daftar


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
    Mengubah (mutate) daftar asli secara langsung.
    """
    if 0 <= index < len(daftar):
        daftar.pop(index)
    return daftar


def balik(daftar: List[Any]) -> List[Any]:
    """
    Membalik urutan elemen dalam daftar.
    """
    return daftar[::-1]
