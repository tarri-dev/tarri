import sqlite3
import os

# ANSI warna
MERAH = "\033[91m"
BIRU = "\033[94m"
RESET = "\033[0m"

# Global state
_LAST_DB_PATH = None

def get_db_path():
    global _LAST_DB_PATH
    return _LAST_DB_PATH

def BuatBasisData(lokasi, nama_db):
    global _LAST_DB_PATH
    try:
        os.makedirs(lokasi, exist_ok=True)
        path = os.path.join(lokasi, nama_db)

        # simpan path ke global
        _LAST_DB_PATH = path  

        if os.path.exists(path):
            i = f"\n{MERAH}[tarri] Basisdata dengan nama '{nama_db}' sudah ada.\n       Lokasi: {path}\n       Basisdata tidak dibuat ulang.{RESET}\n"
            return "gagal", i

        sqlite3.connect(path).close()
        i = f"\n{BIRU}[tarri] Basisdata '{nama_db}' berhasil dibuat.\n       Lokasi: {path}{RESET}\n"
        return "sukses", i
    except Exception as e:
        i = f"\n{MERAH}[tarri] Gagal membuat basisdata '{nama_db}'.\n       Lokasi: {os.path.join(lokasi, nama_db)}\n       Error: {str(e)}{RESET}\n"
        return "gagal", i
