#==============================================================================#
# File    : sqlite.py                                                          #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Komponen internal bahasa pemrograman Tarri.                                #
#==============================================================================#

import sqlite3
import os
import datetime
import json
import re


# =======================================================
# KELAS TABEL
# =======================================================
class Tabel:
    def __init__(self):
        self.fields = []
        self.types = {}

    def untuk(self, tipe):
        self._current_type = tipe
        return self

    def id(self, nama):
        self.fields.append(f"{nama} INTEGER PRIMARY KEY AUTOINCREMENT")
        self.types[nama] = "id (ditulis langsung berurutan)"
        return self

    def kata(self, nama):
        self.fields.append(f"{nama} TEXT")
        self.types[nama] = "[tarri | sqlite] kata (kata maksimal 160 karakter)"
        return self

    def angka(self, nama):
        self.fields.append(f"{nama} INTEGER")
        self.types[nama] = "[tarri | sqlite] angka (bilangan bulat)"
        return self

    def kalimat(self, nama):
        self.fields.append(f"{nama} TEXT")
        self.types[nama] = "[tarri | sqlite] kalimat (kalimat panjang)"
        return self

    def pilihan(self, nama, opsi):
        nama_bersih = re.sub(r"[^0-9A-Za-z_]", "_", nama.strip())
        opsi_str = ", ".join([f"'{o.replace('\'', '\'\'')}'" for o in opsi])
        self.fields.append(
            f'"{nama_bersih}" TEXT CHECK("{nama_bersih}" IN ({opsi_str}))'
        )
        self.types[nama_bersih] = f"pilihan {opsi}"
        return self

    def waktu(self):
        self.fields.append("dibuat TEXT")
        self.fields.append("diubah TEXT")
        self.types["dibuat"] = "[tarri | sqlite] waktu (waktu data dibuat)"
        self.types["diubah"] = "[tarri | sqlite] waktu (waktu data diubah)"
        return self

    def hasil(self):
        return ", ".join(self.fields)

    def __str__(self):
        teks = "Struktur Tabel:\n"
        for kol, tipe in self.types.items():
            teks += f" - {kol:<15} → {tipe}\n"
        return teks.strip()

    __repr__ = __str__


# =======================================================
# KELAS SQLITEHANDLER (FINAL ROBUST VERSION)
# =======================================================
class SQLiteHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_path = None
        self.table_name = None

        # filter state
        self.where_clause = []
        self.where_values = []
        self._or_clauses = []
        self._last_error = None

    def log(self, msg):
        print(f"[tarri | sqlite] {msg}")

    # Helper: Reset filter state
    def _reset_filter(self):
        self.where_clause, self.where_values, self._or_clauses = [], [], []

    # Helper: Sanitasi nama tabel dan kolom untuk cegah SQL Injection
    def _sanitize_ident(self, ident):
        ident_str = str(ident).replace('"', "").replace("'", "").strip()
        # Hanya izinkan huruf, angka, dan underscore
        aman = "".join(c for c in ident_str if c.isalnum() or c == "_")
        if not aman:
            raise Exception(f"Identifier tidak valid (harus alfanumerik): {ident}")
        return f'"{aman}"'

    # Helper: Build WHERE + params
    def _build_where_clause(self):
        conditions = []
        params = []
        if self.where_clause:
            conditions.extend(self.where_clause)
            params.extend(self.where_values)
        if self._or_clauses:
            or_parts = []
            # FIX: _or_clauses selalu berisi 3 elemen: (kolom, operator, nilai)
            for kol, op, val in self._or_clauses:
                kol_quoted = self._sanitize_ident(kol)
                or_parts.append(f"{kol_quoted} {op} ?")
                if op == "LIKE":
                    params.append(f"%{val}%")
                else:
                    params.append(val)
            conditions.append("(" + " OR ".join(or_parts) + ")")
        if not conditions:
            return "", tuple()
        where_sql = " WHERE " + " AND ".join(conditions)
        return where_sql, tuple(params)

    # -------------------------
    # koneksi database
    # -------------------------
    def __koneksi__(self, lokasi, nama_db, nama_tabel):
        try:
            if not os.path.exists(lokasi):
                os.makedirs(lokasi)
            self.db_path = os.path.join(lokasi, f"{nama_db}.sqlite")
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.table_name = nama_tabel
            self.log(f"Koneksi ke '{self.db_path}' berhasil (sukses)")
            return self
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Koneksi ke basis data tidak berhasil (gagal) | {e}")
            return None

    # -------------------------
    # buat tabel
    # -------------------------
    def __buat__(self, tabel_obj):
        try:
            tabel_aman = self._sanitize_ident(self.table_name)
            sql = f"CREATE TABLE IF NOT EXISTS {tabel_aman} ({tabel_obj.hasil()})"
            self.cursor.execute(sql)
            self.conn.commit()
            self.log(f"Tabel '{self.table_name}' siap digunakan.")
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal membuat tabel: {e}")
            return False

    # -------------------------
    # simpan data
    # -------------------------
    def __simpan__(self, data: dict):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            kolom_waktu = [
                c[1]
                for c in self.cursor.execute(f"PRAGMA table_info({self.table_name})")
            ]
            if "diubah" in kolom_waktu:
                data["diubah"] = now
            if "dibuat" in kolom_waktu and "id" not in data:
                data["dibuat"] = now

            kolom = ", ".join([self._sanitize_ident(k) for k in data.keys()])
            nilai = tuple(data.values())
            placeholder = ", ".join(["?"] * len(data))

            tabel_aman = self._sanitize_ident(self.table_name)
            sql = f"INSERT INTO {tabel_aman} ({kolom}) VALUES ({placeholder})"
            self.cursor.execute(sql, nilai)
            self.conn.commit()
            self.log(f"Data baru disimpan ke tabel '{self.table_name}'.")
            return self
        except Exception as e:
            # FIX: ROLLBACK jika gagal
            if self.conn:
                self.conn.rollback()
            self._last_error = str(e)
            self.log(f"Gagal menyimpan data: {e}")
            return None

    # -------------------------
    # ubah data
    # -------------------------
    def __ubah__(self, data: dict):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            kolom_waktu = [
                c[1]
                for c in self.cursor.execute(f"PRAGMA table_info({self.table_name})")
            ]
            if "diubah" in kolom_waktu:
                data["diubah"] = now

            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan 'dimana()' atau 'danDimana()' sebelum ubah().")

            set_clause = ", ".join(
                [f"{self._sanitize_ident(k)} = ?" for k in data.keys()]
            )
            where_sql, params = self._build_where_clause()
            tabel_aman = self._sanitize_ident(self.table_name)
            sql = f"UPDATE {tabel_aman} SET {set_clause}{where_sql}"
            nilai = tuple(data.values()) + tuple(params)

            self.cursor.execute(sql, nilai)
            self.conn.commit()
            row_count = self.cursor.rowcount

            if row_count == 0:
                self.log("Data tidak ditemukan untuk diperbarui.")
                return False

            self.log(
                f"Data pada tabel '{self.table_name}' berhasil diperbarui ({row_count} baris)."
            )
            return self
        except Exception as e:
            # FIX: ROLLBACK jika gagal
            if self.conn:
                self.conn.rollback()
            self._last_error = str(e)
            self.log(f"Gagal memperbarui data: {e}")
            return None
        finally:
            self._reset_filter()

    # -------------------------
    # delete (hapus)
    # -------------------------
    def __hapus__(self):
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan 'dimana()' sebelum hapus()")

            tabel_aman = self._sanitize_ident(self.table_name)
            base_sql = f"DELETE FROM {tabel_aman}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql

            self.cursor.execute(sql, params)
            self.conn.commit()

            row_count = self.cursor.rowcount

            if row_count == 0:
                self.log(
                    f"Tidak ada data yang cocok untuk dihapus dari tabel '{self.table_name}'."
                )
                return False

            self.log(
                f"Data dihapus dari tabel '{self.table_name}' ({row_count} baris)."
            )
            return self
        except Exception as e:
            # FIX: ROLLBACK jika gagal
            if self.conn:
                self.conn.rollback()
            self._last_error = str(e)
            self.log(f"Gagal menghapus data: {e}")
            return None
        finally:
            self._reset_filter()

    # -------------------------
    # helper aman untuk dict (Tidak Berubah)
    # -------------------------
    def _safe_dict(self, kolom, row):
        hasil = {}
        for i, k in enumerate(kolom):
            key = str(k)
            value = row[i]
            if value is None:
                value = ""
            if isinstance(value, (list, tuple)):
                value = json.dumps(value, ensure_ascii=False)
            hasil[key] = value
        return hasil

    # -------------------------
    # ambil semua data (ambil, semua)
    # -------------------------
    def __ambil__(self):
        try:
            tabel_aman = self._sanitize_ident(self.table_name)
            base_sql = f"SELECT * FROM {tabel_aman}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql

            self.cursor.execute(sql, params)
            kolom = (
                [desc[0] for desc in self.cursor.description]
                if self.cursor.description
                else []
            )
            baris = self.cursor.fetchall()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            return False
        finally:
            self._reset_filter()

    # -------------------------
    # ambil 1 (pertama)
    # -------------------------
    def __pertama__(self):
        try:
            tabel_aman = self._sanitize_ident(self.table_name)
            base_sql = f"SELECT * FROM {tabel_aman}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql + " LIMIT 1"

            self.cursor.execute(sql, params)
            if not self.cursor.description:
                return None

            kolom = [desc[0] for desc in self.cursor.description]
            baris = self.cursor.fetchone()

            if not baris:
                return None

            return self._safe_dict(kolom, baris)
        except Exception as e:
            self._last_error = str(e)
            return False
        finally:
            self._reset_filter()

    # -------------------------
    # rapi() (Mengembalikan JSON format)
    # -------------------------
    def __rapi__(self):
        try:
            data = self.__ambil__()
            if data is False:
                return False
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            self._last_error = str(e)
            return False

    # -------------------------
    # tampilkan tabel (Mengembalikan tabel ASCII rapi)
    # -------------------------
    def __tabel__(self):
        try:
            data = self.__ambil__()  # Menggunakan __ambil__ yang sudah reset filter

            if data is False:
                return f"[tarri | sqlite] Gagal mengambil data: {self._last_error}"

            if not data:
                return "[tarri | sqlite] Tidak ada data dalam tabel."

            kolom = list(data[0].keys())
            baris = [list(d.values()) for d in data]

            # Hitung lebar maksimum
            lebar = []
            for i, k in enumerate(kolom):
                max_lebar_data = max(len(str(r[i])) for r in baris)
                lebar.append(max(len(str(k)), max_lebar_data))

            # Buat garis pemisah
            garis = "+".join("-" * (l + 2) for l in lebar)
            teks = f"+{garis}+\n"

            # Baris Header
            header_parts = [f"{k:<{lebar[i]}}" for i, k in enumerate(kolom)]
            teks += "| " + " | ".join(header_parts) + " |\n"
            teks += f"+{garis}+\n"

            # Baris Data
            for r in baris:
                row_parts = [f"{str(r[i]):<{lebar[i]}}" for i in range(len(kolom))]
                teks += "| " + " | ".join(row_parts) + " |\n"

            teks += f"+{garis}+"
            return teks
        except Exception as e:
            self._last_error = str(e)
            return f"[tarri | sqlite] Gagal menampilkan tabel: {e}"

    # -------------------------
    # urutkan()
    # -------------------------
    def __urutkan__(self, arah="a-z", kolom="id"):
        try:
            arah_sql = "ASC" if arah.lower() == "a-z" else "DESC"
            tabel_aman = self._sanitize_ident(self.table_name)
            kolom_aman = self._sanitize_ident(kolom)

            base_sql = f"SELECT * FROM {tabel_aman}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql + f" ORDER BY {kolom_aman} {arah_sql}"

            self.cursor.execute(sql, params)
            kolom = (
                [desc[0] for desc in self.cursor.description]
                if self.cursor.description
                else []
            )
            baris = self.cursor.fetchall()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal mengurutkan data: {e}")
            return False
        finally:
            self._reset_filter()

    # -------------------------
    # filter helpers (dimana, danDimana, atauDimana)
    # -------------------------
    def __dimana__(self, kolom, nilai):
        kol_quoted = self._sanitize_ident(kolom)
        self._reset_filter()

        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause = [f"{kol_quoted} LIKE ?"]
            self.where_values = [f"%{nilai}%"]
        else:
            self.where_clause = [f"{kol_quoted} = ?"]
            self.where_values = [nilai]

        return self

    def __danDimana__(self, kolom, nilai):
        kol_quoted = self._sanitize_ident(kolom)

        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause.append(f"{kol_quoted} LIKE ?")
            self.where_values.append(f"%{nilai}%")
        else:
            self.where_clause.append(f"{kol_quoted} = ?")
            self.where_values.append(nilai)

        return self

    def __atauDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            clause = (kolom, "LIKE", nilai)
        else:
            clause = (kolom, "=", nilai)

        self._or_clauses.append(clause)
        return self

    # -------------------------
    # TUTUP KONEKSI
    # -------------------------
    def __tutup__(self):
        """Menutup koneksi SQLite secara eksplisit untuk melepaskan file lock."""
        try:
            if self.conn:
                # Tutup koneksi, yang juga menutup kursor
                self.conn.close()
                self.conn = None
                self.cursor = None
                self.log("Koneksi SQLite ditutup dengan bersih. File lock dilepaskan.")
                return True
            return False
        except Exception as e:
            self.log(f"Gagal menutup koneksi SQLite: {e}")
            return False

    # -------------------------
    # ALIAS PUBLIK
    # -------------------------
    tutup = __tutup__
    koneksi = __koneksi__
    buat = __buat__
    simpan = __simpan__
    ubah = __ubah__
    hapus = __hapus__

    # Filter aliases
    dimana = __dimana__
    danDimana = __danDimana__
    atauDimana = __atauDimana__

    # Fetch aliases
    ambil = __ambil__
    pertama = __pertama__
    semua = __ambil__
    rapi = __rapi__
    tabel = __tabel__
    urutkan = __urutkan__


# =======================================================
# FACTORY DAN ALIAS AKHIR
# =======================================================
class SQLiteFactory:
    """Kelas pembantu yang dipanggil oleh interpreter Tarri"""

    def koneksi(self, lokasi, nama_db, nama_tabel):
        """Membuat instance SQLiteHandler baru dan mencoba koneksi. Mengembalikan objek handler."""
        handler = SQLiteHandler()
        return handler.__koneksi__(lokasi, nama_db, nama_tabel)


# Alias akhir yang dieksekusi oleh interpreter Tarri
sqlite = SQLiteFactory()
tabel_sqlite = Tabel
