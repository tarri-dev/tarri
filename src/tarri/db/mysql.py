# import mysql.connector
import mysql.connector as mysql_connector
from mysql.connector import Error
import datetime
import json

class Tabel:
    def __init__(self):
        self.fields = []
        self.types = {}

    def id(self, nama):
        self.fields.append(f"`{nama}` INT AUTO_INCREMENT PRIMARY KEY")
        self.types[nama] = "[tarri | mysql] id (terisi secara otomatis)"
        return self

    def kata(self, nama):
        self.fields.append(f"`{nama}` VARCHAR(255)")
        self.types[nama] = "[tarri | mysql] kata"
        return self

    def angka(self, nama):
        self.fields.append(f"`{nama}` INT")
        self.types[nama] = "[tarri | mysql] angka"
        return self

    def kalimat(self, nama):
        self.fields.append(f"`{nama}` TEXT")
        self.types[nama] = "[tarri | mysql] kalimat"
        return self
    
    def pilihan(self, nama, opsi):
        opsi_str = ", ".join([f"'{o}'" for o in opsi])
        self.fields.append(f"`{nama}` ENUM({opsi_str})")
        self.types[nama] = f"[tarri | mysql] pilihan {opsi}"
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


class MySQLHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.table_name = None

        self.where_clause = []
        self.where_values = []
        self._or_clauses = []

    def log(self, msg):
        print(f"[tarri | mysql] {msg}")

    # -------------------------------------------------------
    # koneksi
    # -------------------------------------------------------
    def __koneksi__(self, host, user, password, database, table):
        try:
            self.conn = mysql_connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cursor = self.conn.cursor()
            self.table_name = table
            self.log(f"Koneksi ke MySQL '{database}' berhasil.")
            return True
        except Error as e:
            self.log(f"Gagal koneksi: {e}")
            return False

    # -------------------------------------------------------
    # buat tabel
    # -------------------------------------------------------
    def __buat__(self, tabel_obj):
        try:
            sql = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({tabel_obj.hasil()})"
            self.cursor.execute(sql)
            self.conn.commit()
            self.log(f"Tabel '{self.table_name}' siap digunakan.")
            return True
        except Exception as e:
            self.log(f"Gagal membuat tabel: {e}")
            return False

    # -------------------------------------------------------
    # simpan (INSERT)
    # -------------------------------------------------------
    def __simpan__(self, data: dict):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # auto set waktu
            cols = self._cek_kolom()
            if "dibuat" in cols and "id" not in data:
                data["dibuat"] = now
            if "diubah" in cols:
                data["diubah"] = now

            kolom = ", ".join([f"`{k}`" for k in data.keys()])
            placeholder = ", ".join(["%s"] * len(data))
            nilai = list(data.values())

            sql = f"INSERT INTO `{self.table_name}` ({kolom}) VALUES ({placeholder})"
            self.cursor.execute(sql, nilai)
            self.conn.commit()

            self.log("Data disimpan.")
            return True
        except Exception as e:
            self.log(f"Gagal menyimpan data: {e}")
            return False

    # -------------------------------------------------------
    # ubah (UPDATE)
    # -------------------------------------------------------
    def __ubah__(self, data: dict):
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan dimana() sebelum ubah().")

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cols = self._cek_kolom()
            if "diubah" in cols:
                data["diubah"] = now

            set_sql = ", ".join([f"`{k}`=%s" for k in data.keys()])
            where_sql, params = self._build_where()

            sql = f"UPDATE `{self.table_name}` SET {set_sql}{where_sql}"
            self.cursor.execute(sql, list(data.values()) + params)
            self.conn.commit()

            self.log("Data diperbarui.")
            return True
        except Exception as e:
            self.log(f"Gagal mengubah data: {e}")
            return False
        finally:
            self._reset()

    # -------------------------------------------------------
    # hapus (DELETE)
    # -------------------------------------------------------
    def __hapus__(self):
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan dimana() sebelum hapus().")

            where_sql, params = self._build_where()
            sql = f"DELETE FROM `{self.table_name}`{where_sql}"

            self.cursor.execute(sql, params)
            self.conn.commit()

            self.log("Data dihapus.")
            return True
        except Exception as e:
            self.log(f"Gagal menghapus data: {e}")
            return False
        finally:
            self._reset()

    # -------------------------------------------------------
    # ambil (SELECT)
    # -------------------------------------------------------
    def __ambil__(self):
        try:
            where_sql, params = self._build_where()
            sql = f"SELECT * FROM `{self.table_name}`{where_sql}"

            self.cursor.execute(sql, params)
            kolom = [c[0] for c in self.cursor.description]
            baris = self.cursor.fetchall()
            self._reset()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self.log(f"Gagal ambil: {e}")
            return False

    def __pertama__(self):
        try:
            where_sql, params = self._build_where()
            sql = f"SELECT * FROM `{self.table_name}`{where_sql} LIMIT 1"

            self.cursor.execute(sql, params)
            kolom = [c[0] for c in self.cursor.description]
            row = self.cursor.fetchone()
            self._reset()

            if not row:
                return None

            return self._safe_dict(kolom, row)
        except Exception as e:
            self.log(f"Gagal pertama: {e}")
            return False
        
    # -------------------------
    # semua() 
    # -------------------------

    def __semua__(self):
        return self.__ambil__()
    
    # -------------------------
    # rapi() — json pretty print (menghormati filter)
    # -------------------------
    def __rapi__(self):
        try:
            data = self.__semua__()  # __semua__ sudah menangani filter + reset
            if data is False:
                return False
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            self._last_error = str(e)
            return False
        
    # -------------------------
    # tampilkan tabel (text) — juga menghormati filter
    # -------------------------
    def __tabel__(self):
        try:
            data = self.__semua__()
            if not data:
                return "[tarri | mysql] Tidak ada data dalam tabel."

            kolom = list(data[0].keys())
            baris = [list(d.values()) for d in data]

            lebar = [
                max(len(str(k)), max(len(str(r[i])) for r in baris))
                for i, k in enumerate(kolom)
            ]

            garis = "+".join("-" * (l + 2) for l in lebar)
            teks = f"+{garis}+\n"
            teks += "| " + " | ".join(f"{k:<{lebar[i]}}" for i, k in enumerate(kolom)) + " |\n"
            teks += f"+{garis}+\n"

            for r in baris:
                teks += "| " + " | ".join(f"{str(r[i]):<{lebar[i]}}" for i in range(len(kolom))) + " |\n"

            teks += f"+{garis}+"
            return teks

        except Exception as e:
            self._last_error = str(e)
            return f"[tarri | mysql] Gagal menampilkan tabel: {e}"



    # -------------------------------------------------------
    # urutkan
    # -------------------------------------------------------
    def __urutkan__(self, arah="a-z", kolom="id"):
        try:
            arah_sql = "ASC" if arah == "a-z" else "DESC"
            where_sql, params = self._build_where()

            sql = f"SELECT * FROM `{self.table_name}`{where_sql} ORDER BY `{kolom}` {arah_sql}"

            self.cursor.execute(sql, params)
            kolom = [c[0] for c in self.cursor.description]
            baris = self.cursor.fetchall()
            self._reset()

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self.log(f"Gagal urutkan: {e}")
            return False

    # -------------------------------------------------------
    # FILTER (LIKE minimal 3 huruf)
    # -------------------------------------------------------
    def __dimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause = [f"`{kolom}` LIKE %s"]
            self.where_values = [f"%{nilai}%"]
            self.log(f"Dimana Seperti: {kolom} '%{nilai}%'")
        else:
            self.where_clause = [f"`{kolom}`=%s"]
            self.where_values = [nilai]
            self.log(f"Dimana Exact: {kolom} = {nilai}")
        return True

    def __danDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            self.where_clause.append(f"`{kolom}` LIKE %s")
            self.where_values.append(f"%{nilai}%")
            self.log(f"Dan Seperti: {kolom}")
        else:
            self.where_clause.append(f"`{kolom}`=%s")
            self.where_values.append(nilai)
            self.log(f"Dan Exact: {kolom}")
        return True

    def __atauDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            self._or_clauses.append((kolom, "LIKE", f"%{nilai}%"))
            self.log(f"Atau Seperti: {kolom}")
        else:
            self._or_clauses.append((kolom, "=", nilai))
            self.log(f"Atau Exact: {kolom}")
        return True

    # -------------------------------------------------------
    # Helper
    # -------------------------------------------------------
    def _cek_kolom(self):
        self.cursor.execute(f"DESCRIBE `{self.table_name}`")
        return [c[0] for c in self.cursor.fetchall()]

    def _build_where(self):
        kondisi = []
        params = []

        if self.where_clause:
            kondisi.extend(self.where_clause)
            params.extend(self.where_values)

        if self._or_clauses:
            or_sql = []
            for kol, op, val in self._or_clauses:
                or_sql.append(f"`{kol}` {op} %s")
                params.append(val)
            kondisi.append("(" + " OR ".join(or_sql) + ")")

        if not kondisi:
            return "", []

        return " WHERE " + " AND ".join(kondisi), params

    def _safe_dict(self, kolom, row):
        data = {}
        for i, k in enumerate(kolom):
            v = row[i]
            if v is None:
                v = ""
            data[str(k)] = v
        return data

    def _reset(self):
        self.where_clause = []
        self.where_values = []
        self._or_clauses = []


# alias agar sama seperti SQLite
mysql = MySQLHandler()
tabel_mysql = Tabel

mysql.koneksi = mysql.__koneksi__
mysql.buat    = mysql.__buat__
mysql.simpan  = mysql.__simpan__
mysql.ubah    = mysql.__ubah__
mysql.ambil   = mysql.__ambil__
mysql.semua   = mysql.__semua__
mysql.pertama = mysql.__pertama__
mysql.rapi    = mysql.__rapi__
mysql.tabel   = mysql.__tabel__
mysql.hapus   = mysql.__hapus__
mysql.dimana  = mysql.__dimana__
mysql.danDimana = mysql.__danDimana__
mysql.atauDimana = mysql.__atauDimana__
mysql.urutkan = mysql.__urutkan__
