#==============================================================================#
# File    : slug.py                                                            #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'slug' yang tersedia dalam bahasa Tarri.        #
#==============================================================================#

import re
import unicodedata


def slug(teks: str) -> str:
    """
    Mengubah teks menjadi URL-friendly slug.

    Contoh:
        "Halo Dunia TARRI" -> "halo-dunia-tarri"
    """
    # 1. Normalize unicode, hilangkan aksen
    teks = unicodedata.normalize("NFKD", teks)
    teks = teks.encode("ascii", "ignore").decode("ascii")

    # 2. Lowercase
    teks = teks.lower()

    # 3. Ganti spasi / karakter non-alphanumeric jadi -
    teks = re.sub(r"[^a-z0-9]+", "-", teks)

    # 4. Hapus - di awal & akhir
    teks = teks.strip("-")

    return teks
