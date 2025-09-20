# tarri/src/tarri/database/buattabel.py
import sqlite3
import os
from tarri.database.buatbasisdata import get_db_path

# --------------------------
# Context DB (diinject dari interpreter)
# --------------------------
DB_CONTEXT = {}

def set_db_context(ctx: dict):
    """Inject context runtime dari interpreter TARRI"""
    global DB_CONTEXT
    DB_CONTEXT = ctx


def get_table_name():
    """Ambil nama tabel dari context"""
    return DB_CONTEXT.get("_bd_tabel")


class BasisData:
    def __init__(self):
        self.columns = []

    def id(self):
        """Kolom primary key auto-increment"""
        self.columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        return self

    def kata(self, nama):
        """Kolom teks bebas"""
        self.columns.append(f"{nama} TEXT")
        return self

    def angka(self, nama):
        """Kolom angka integer"""
        self.columns.append(f"{nama} INTEGER")
        return self

    def desimal(self, nama):
        """Kolom angka desimal"""
        self.columns.append(f"{nama} REAL")
        return self

    def logika(self, nama):
        """Kolom logika, hanya 0 atau 1"""
        self.columns.append(f"{nama} INTEGER CHECK({nama} IN (0,1))")
        return self

    def pilihan(self, nama, opsi: list):
        """
        Kolom pilihan dengan constraint case-insensitive.
        Input user boleh huruf besar/kecil, tapi akan disimpan lowercase.
        """
        opsi_lower = ",".join(f"'{o.lower()}'" for o in opsi)
        # gunakan LOWER() di constraint agar case-insensitive
        # INSERT akan otomatis LOWER saat eksekusi query
        self.columns.append(
            f"{nama} TEXT CHECK(LOWER({nama}) IN ({opsi_lower}))"
        )
        return self


    def waktu(self):
        """Kolom waktu otomatis"""
        self.columns.append("dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        self.columns.append("diubah TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        return self


# --------------------------
# Fungsi BuatTabel
# --------------------------
def BuatTabel(*args):
    try:
        # Pastikan arg terakhir adalah BasisData
        if len(args) == 1:
            bd_obj = args[0]
            if not isinstance(bd_obj, BasisData):
                return "gagal", "[ERROR BuatTabel] Argumen terakhir harus BasisData."
            nama_db = get_db_path()
            nama_tabel = get_table_name()
        elif len(args) == 2:
            nama_tabel, bd_obj = args
            if not isinstance(bd_obj, BasisData):
                return "gagal", "[ERROR BuatTabel] Argumen terakhir harus BasisData."
            nama_db = get_db_path()
        elif len(args) == 3:
            nama_db, nama_tabel, bd_obj = args
            if not isinstance(bd_obj, BasisData):
                return "gagal", "[ERROR BuatTabel] Argumen terakhir harus BasisData."
        else:
            return "gagal", "[ERROR BuatTabel] Jumlah argumen tidak valid."

        if not nama_db:
            return "gagal", "[ERROR BuatTabel] BasisData belum diinisialisasi."
        if not nama_tabel:
            return "gagal", "[ERROR BuatTabel] Nama tabel belum diberikan."

        conn = sqlite3.connect(nama_db)
        cur = conn.cursor()
        kolom_str = ", ".join(bd_obj.columns)
        cur.execute(f"CREATE TABLE IF NOT EXISTS {nama_tabel} ({kolom_str})")
        conn.commit()
        conn.close()

        i = f"Tabel '{nama_tabel}' berhasil dibuat di {nama_db}"
        return "sukses", i
    except Exception as e:
        i = f"[ERROR BuatTabel] {e}"
        return "gagal", i



# --------------------------
# Fungsi HapusTabel
# --------------------------
def HapusTabel(nama_db, nama_tabel, lokasi_db=None):
    import sqlite3, os
    try:
        if not nama_db or not nama_tabel:
            return "gagal"

        # pastikan path database valid
        if lokasi_db:
            db_path = os.path.join(lokasi_db, nama_db)
        else:
            db_path = nama_db  # fallback

        if not os.path.exists(db_path):
            print(f"[DEBUG] Database {db_path} tidak ditemukan")
            return "gagal"

        # koneksi dan drop tabel
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f'DROP TABLE IF EXISTS "{nama_tabel}"')
        conn.commit()
        conn.close()

        return "sukses"

    except Exception as e:
        print(f"[ERROR HapusTabel] {e}")
        return "gagal"
