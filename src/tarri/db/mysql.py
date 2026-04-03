#==============================================================================#
# File    : mysql.py                                                           #
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

# import mysql.connector
import mysql.connector as mysql_connector
from mysql.connector import Error
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

    def id(self, nama):
        self.fields.append(f"`{nama}` INT AUTO_INCREMENT PRIMARY KEY")
        self.types[nama] = "[tarri | mysql] id (terisi secara otomatis)"
        return self

    def kata(self, nama):
        self.fields.append(f"`{nama}` VARCHAR(160)")
        self.types[nama] = "[tarri | mysql] kata (maksimal 160 karakter)"
        return self

    def angka(self, nama):
        self.fields.append(f"`{nama}` INT")
        self.types[nama] = "[tarri | mysql] angka (bilangan bulat)"
        return self

    def kalimat(self, nama):
        self.fields.append(f"`{nama}` TEXT")
        self.types[nama] = "[tarri | mysql] kalimat (kalimat panjang)"
        return self

    def pilihan(self, nama, opsi):
        nama_bersih = re.sub(r"[^0-9A-Za-z_]", "_", nama.strip())
        opsi_str = ", ".join([f"'{o.replace('\'', '\'\'')}'" for o in opsi])
        self.fields.append(f"`{nama_bersih}` ENUM({opsi_str})")
        self.types[nama_bersih] = f"[tarri | mysql] pilihan {opsi}"
        return self

    def waktu(self):
        self.fields.append("dibuat TEXT")
        self.fields.append("diubah TEXT")
        self.types["dibuat"] = "[tarri | mysql] waktu (waktu data dibuat)"
        self.types["diubah"] = "[tarri | mysql] waktu (waktu data diubah)"
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
# KELAS MYSQLHANDLER (DIREVISI TOTAL UNTUK KONEKSI PER-OPERASI)
# =======================================================
class MySQLHandler:
    def __init__(self):
        self.config = {}  # Menyimpan parameter koneksi
        self.table_name = None

        self.where_clause = []
        self.where_values = []
        self._or_clauses = []
        self._last_error = None

    def log(self, msg):
        print(f"[tarri | mysql] {msg}")

    # Helper: RESET filter state
    def _reset(self):
        self.where_clause = []
        self.where_values = []
        self._or_clauses = []

    # Helper: AMBIL KONEKSI BARU DAN KURATOR
    def _get_conn_cursor(self):
        """Membuka koneksi dan kursor baru untuk satu operasi."""
        if not self.config:
            raise Error("Konfigurasi koneksi belum diatur.")

        conn = None
        try:
            conn = mysql_connector.connect(**self.config)
            cursor = conn.cursor()
            return conn, cursor
        except Error as e:
            # Penting: Tutup koneksi jika gagal mendapatkan kursor
            if conn:
                conn.close()
            raise Error(f"Gagal mendapatkan koneksi/kursor: {e}")

    # Helper: Build WHERE + params
    def _build_where(self):
        conditions = []
        params = []
        if self.where_clause:
            conditions.extend(self.where_clause)
            params.extend(self.where_values)
        if self._or_clauses:
            or_parts = []
            for kol, op, val in self._or_clauses:
                kol_quoted = f"`{kol}`"
                or_parts.append(f"{kol_quoted} {op} %s")
                params.append(val)
            conditions.append("(" + " OR ".join(or_parts) + ")")

        if not conditions:
            return "", []

        where_sql = " WHERE " + " AND ".join(conditions)
        return where_sql, params

    # Helper: Cek kolom (menggunakan koneksi sementara)
    def _cek_kolom(self, cursor):
        try:
            cursor.execute(f"DESCRIBE `{self.table_name}`")
            return [c[0] for c in cursor.fetchall()]
        except Exception:
            return []

    # Helper: Safe Dict
    def _safe_dict(self, kolom, row):
        data = {}
        for i, k in enumerate(kolom):
            v = row[i]
            if v is None:
                v = ""
            data[str(k)] = v
        return data

    # -------------------------------------------------------
    # koneksi (Setup Awal Konfigurasi)
    # -------------------------------------------------------
    def __koneksi__(self, host, user, password, database, table):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }
        self.table_name = table

        # Tes koneksi dan tutup segera (agar tidak bocor saat inisialisasi)
        try:
            temp_conn = mysql_connector.connect(**self.config)
            temp_conn.close()
            self.log(f"Koneksi ke MySQL '{database}' berhasil (konfigurasi disimpan).")
            return self
        except Error as e:
            self._last_error = str(e)
            self.log(f"Gagal koneksi: {e}")
            return None

    # -------------------------------------------------------
    # buat tabel (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __buat__(self, tabel_obj):
        conn = None
        try:
            conn, cursor = self._get_conn_cursor()
            sql = (
                f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({tabel_obj.hasil()})"
            )
            cursor.execute(sql)
            conn.commit()
            self.log(f"Tabel '{self.table_name}' siap digunakan.")
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal membuat tabel: {e}")
            return False
        finally:
            # 🛑 WAJIB TUTUP KONEKSI YANG BARU DIBUKA
            if conn:
                conn.close()

    # -------------------------------------------------------
    # simpan (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __simpan__(self, data: dict):
        conn = None
        try:
            conn, cursor = self._get_conn_cursor()

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cols = self._cek_kolom(cursor)  # Gunakan cursor dari koneksi baru
            if "dibuat" in cols and "id" not in data:
                data["dibuat"] = now
            if "diubah" in cols:
                data["diubah"] = now

            kolom = ", ".join([f"`{k}`" for k in data.keys()])
            placeholder = ", ".join(["%s"] * len(data))
            nilai = list(data.values())

            sql = f"INSERT INTO `{self.table_name}` ({kolom}) VALUES ({placeholder})"
            cursor.execute(sql, nilai)
            conn.commit()

            self.log("Data disimpan.")
            return self
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal menyimpan data: {e}")
            return None
        finally:
            # 🛑 WAJIB TUTUP KONEKSI YANG BARU DIBUKA
            if conn:
                conn.close()
            self._reset()

    # -------------------------------------------------------
    # ubah (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __ubah__(self, data: dict):
        conn = None
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan dimana() atau danDimana() sebelum ubah().")

            conn, cursor = self._get_conn_cursor()

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cols = self._cek_kolom(cursor)
            if "diubah" in cols:
                data["diubah"] = now

            set_sql = ", ".join([f"`{k}`=%s" for k in data.keys()])
            where_sql, params = self._build_where()

            sql = f"UPDATE `{self.table_name}` SET {set_sql}{where_sql}"
            cursor.execute(sql, list(data.values()) + params)
            conn.commit()

            row_count = cursor.rowcount

            if row_count == 0:
                self.log("Data tidak ditemukan untuk diperbarui.")
                return False

            self.log(f"Data diperbarui ({row_count} baris).")
            return self
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal mengubah data: {e}")
            return None
        finally:
            if conn:
                conn.close()
            self._reset()

    # -------------------------------------------------------
    # hapus (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __hapus__(self):
        conn = None
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan dimana() sebelum hapus()")

            conn, cursor = self._get_conn_cursor()

            where_sql, params = self._build_where()
            sql = f"DELETE FROM `{self.table_name}`{where_sql}"

            cursor.execute(sql, params)
            conn.commit()

            row_count = cursor.rowcount

            if row_count == 0:
                self.log(
                    f"Tidak ada data yang cocok untuk dihapus dari tabel '{self.table_name}'."
                )
                return False

            self.log(f"Data dihapus ({row_count} baris).")
            return self
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal menghapus data: {e}")
            return None
        finally:
            if conn:
                conn.close()
            self._reset()

    # -------------------------------------------------------
    # ambil (SELECT) (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __ambil__(self):
        conn = None
        try:
            where_sql, params = self._build_where()
            sql = f"SELECT * FROM `{self.table_name}`{where_sql}"

            conn, cursor = self._get_conn_cursor()

            cursor.execute(sql, params)
            kolom = [c[0] for c in cursor.description]
            baris = cursor.fetchall()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal ambil: {e}")
            return False
        finally:
            if conn:
                conn.close()
            self._reset()

    def __pertama__(self):
        conn = None
        try:
            where_sql, params = self._build_where()
            sql = f"SELECT * FROM `{self.table_name}`{where_sql} LIMIT 1"

            conn, cursor = self._get_conn_cursor()

            cursor.execute(sql, params)

            if not cursor.description:
                return None

            kolom = [c[0] for c in cursor.description]
            row = cursor.fetchone()

            if not row:
                return None

            return self._safe_dict(kolom, row)
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal pertama: {e}")
            return False
        finally:
            if conn:
                conn.close()
            self._reset()

    # -------------------------------------------------------
    # urutkan (Koneksi Per-Operasi)
    # -------------------------------------------------------
    def __urutkan__(self, arah="a-z", kolom="id"):
        conn = None
        try:
            arah_sql = "ASC" if arah == "a-z" else "DESC"
            where_sql, params = self._build_where()

            sql = f"SELECT * FROM `{self.table_name}`{where_sql} ORDER BY `{kolom}` {arah_sql}"

            conn, cursor = self._get_conn_cursor()

            cursor.execute(sql, params)
            kolom = [c[0] for c in cursor.description]
            baris = cursor.fetchall()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal urutkan: {e}")
            return False
        finally:
            if conn:
                conn.close()
            self._reset()

    # -------------------------------------------------------
    # FUNGSI TUTUP (Menjadi Kosong/Dihapus)
    # -------------------------------------------------------
    # HAPUS FUNGSI __tutup__ karena sekarang penutupan dilakukan
    # otomatis di setiap operasi (di blok 'finally').
    def __tutup__(self):
        self.log(
            "Peringatan: Fungsi tutup() dipanggil, tetapi koneksi ditutup secara otomatis per-operasi."
        )
        return True

    # -------------------------------------------------------
    # FILTER (Tetap sama, hanya mengupdate variabel state)
    # -------------------------------------------------------
    def __dimana__(self, kolom, nilai):
        self._reset()
        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause = [f"`{kolom}` LIKE %s"]
            self.where_values = [f"%{nilai}%"]
        else:
            self.where_clause = [f"`{kolom}`=%s"]
            self.where_values = [nilai]
        return self

    def __danDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause.append(f"`{kolom}` LIKE %s")
            self.where_values.append(f"%{nilai}%")
        else:
            self.where_clause.append(f"`{kolom}`=%s")
            self.where_values.append(nilai)
        return self

    def __atauDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            self._or_clauses.append((kolom, "LIKE", f"%{nilai}%"))
        else:
            self._or_clauses.append((kolom, "=", nilai))
        return self

    # -------------------------------------------------------
    # FUNGSI TAMBAHAN (Tidak menggunakan koneksi, jadi tidak diubah)
    # -------------------------------------------------------
    def __rapi__(self):
        try:
            data = self.__semua__()
            if data is False:
                return False
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            self._last_error = str(e)
            return False

    def __tabel__(self):
        data = self.__semua__()

        if data is False:
            return f"[tarri | mysql] Gagal mengambil data: {self._last_error}"

        if not data:
            return "[tarri | mysql] Tidak ada data dalam tabel."

        try:
            kolom = list(data[0].keys())
            baris = [list(d.values()) for d in data]

            lebar = []
            for i, k in enumerate(kolom):
                max_lebar_data = max(len(str(r[i])) for r in baris)
                lebar.append(max(len(str(k)), max_lebar_data))

            garis = "+".join("-" * (l + 2) for l in lebar)
            teks = f"+{garis}+\n"

            header_parts = []
            for i, k in enumerate(kolom):
                header_parts.append(f"{k:<{lebar[i]}}")
            teks += "| " + " | ".join(header_parts) + " |\n"
            teks += f"+{garis}+\n"

            for r in baris:
                row_parts = []
                for i in range(len(kolom)):
                    row_parts.append(f"{str(r[i]):<{lebar[i]}}")
                teks += "| " + " | ".join(row_parts) + " |\n"

            teks += f"+{garis}+"
            return teks

        except Exception as e:
            self._last_error = str(e)
            return f"[tarri | mysql] Gagal menampilkan tabel: {e}"

    # Alias publik untuk interpreter Tarri
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


class MySQLFactory:
    """Kelas pembantu yang dipanggil oleh interpreter Tarri"""

    def koneksi(self, host, user, password, database, table):
        """Membuat instance MySQLHandler baru dan mencoba koneksi. Mengembalikan objek handler."""
        handler = MySQLHandler()
        return handler.__koneksi__(host, user, password, database, table)


# Alias akhir yang dieksekusi oleh interpreter Tarri
mysql = MySQLFactory()
tabel_mysql = Tabel
