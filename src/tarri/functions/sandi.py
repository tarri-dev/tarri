#==============================================================================#
# File    : sandi.py                                                           #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'sandi' yang tersedia dalam bahasa Tarri.       #
#==============================================================================#

import hashlib
import random
import string

# ================================
# Modul Sandi untuk TARRI
# ================================


def _generate_salt(length=8):
    """Buat salt acak"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def buat_sandi(password, salt=None):
    """
    Hash password dengan SHA512 + salt
    Jika salt tidak diberikan, buat baru.
    Kembalikan string "salt$hash"
    """
    if salt is None:
        salt = _generate_salt()
    hashed = hashlib.sha512((salt + str(password)).encode("utf-8")).hexdigest()
    return f"{salt}${hashed}"


def cek_sandi(password_plain, hash_salt):
    """
    Cek password plain dengan hash yang ada
    """
    try:
        salt, hashed = hash_salt.split("$")
        return (
            hashlib.sha512((salt + str(password_plain)).encode("utf-8")).hexdigest()
            == hashed
        )
    except Exception:
        return False
