import sqlite3
import os
import datetime
import json
import re

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
        nama_bersih = re.sub(r'[^0-9A-Za-z_]', '_', nama.strip())
        opsi_str = ", ".join([f"'{o.replace('\'', '\'\'')}'" for o in opsi])  # escape '
        self.fields.append(f'"{nama_bersih}" TEXT CHECK("{nama_bersih}" IN ({opsi_str}))')
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
    

class SQLiteHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_path = None
        self.table_name = None

        # filter state
        self.where_clause = []    # e.g. ['"email" = ?']
        self.where_values = []    # parameter values for above
        self._or_clauses = []     # list of tuples (col, val) for OR
        self._last_error = None

    def log(self, msg):
        print(f"[tarri | sqlite] {msg}")

    # -------------------------
    # Helper: build WHERE + params
    # -------------------------
    def _build_where_clause(self):
        """
        Bangun klausa WHERE dan params berdasarkan:
         - self.where_clause (AND parts already formatted)
         - self.where_values (params for AND parts)
         - self._or_clauses (list of (col, val) tuples -> OR group)

        Mengembalikan (where_sql_str_or_empty, params_tuple)
        """
        conditions = []
        params = []

        if self.where_clause:
            conditions.extend(self.where_clause)
            params.extend(self.where_values)

        if self._or_clauses:
            or_parts = []
            for kol, val in self._or_clauses:
                # pastikan kol sudah dikutip pada caller; caller biasanya memberikan nama kolom tanpa kutip
                # kita gunakan format yang konsisten: double-quote di sekitar nama kolom
                kol_quoted = f'"{kol}"' if not (kol.startswith('"') and kol.endswith('"')) else kol
                or_parts.append(f'{kol_quoted} = ?')
                params.append(val)
            # gabungkan OR menjadi satu group
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
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Koneksi ke basis data tidak berhasil (gagal) | {e}")
            return False

    # -------------------------
    # buat tabel
    # -------------------------
    def __buat__(self, tabel_obj):
        try:
            sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({tabel_obj.hasil()})"
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
            kolom_waktu = [c[1] for c in self.cursor.execute(f"PRAGMA table_info({self.table_name})")]
            if "diubah" in kolom_waktu:
                data["diubah"] = now
            if "dibuat" in kolom_waktu and "id" not in data:
                data["dibuat"] = now

            kolom = ", ".join([f'"{k}"' for k in data.keys()])
            nilai = tuple(data.values())
            placeholder = ", ".join(["?"] * len(data))

            sql = f"INSERT INTO {self.table_name} ({kolom}) VALUES ({placeholder})"
            self.cursor.execute(sql, nilai)
            self.conn.commit()
            self.log(f"Data baru disimpan ke tabel '{self.table_name}'.")
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal menyimpan data: {e}")
            return False

    # -------------------------
    # ubah data
    # -------------------------
    def __ubah__(self, data: dict):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            kolom_waktu = [c[1] for c in self.cursor.execute(f"PRAGMA table_info({self.table_name})")]
            if "diubah" in kolom_waktu:
                data["diubah"] = now

            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan 'dimana()' atau 'danDimana()' sebelum ubah().")

            set_clause = ", ".join([f'"{k}" = ?' for k in data.keys()])

            # Build where + params
            where_sql, params = self._build_where_clause()

            sql = f'UPDATE "{self.table_name}" SET {set_clause}{where_sql}'
            nilai = tuple(data.values()) + tuple(params)
            self.cursor.execute(sql, nilai)
            self.conn.commit()

            if self.cursor.rowcount == 0:
                self.log("Data tidak ditemukan untuk diperbarui.")
                return False

            self.log(f"Data pada tabel '{self.table_name}' berhasil diperbarui.")
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal memperbarui data: {e}")
            return False
        finally:
            # reset filter state selalu
            self.where_clause, self.where_values, self._or_clauses = [], [], []

    # -------------------------
    # helper aman untuk dict
    # -------------------------
    
    def _safe_dict(self, kolom, row):
        hasil = {}
        for i, k in enumerate(kolom):
            key = str(k)
            value = row[i]

            # KONVERSI None → ""
            if value is None:
                value = ""

            # handle list/tuple agar tidak error
            if isinstance(value, (list, tuple)):
                value = json.dumps(value, ensure_ascii=False)

            hasil[key] = value
        return hasil


    # -------------------------
    # ambil semua data atau dengan filter
    # -------------------------
    def __ambil__(self):
        try:
            base_sql = f"SELECT * FROM {self.table_name}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql

            self.cursor.execute(sql, params)
            kolom = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
            baris = self.cursor.fetchall()

            # reset filter setelah digunakan
            self.where_clause, self.where_values, self._or_clauses = [], [], []

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            return False

    # -------------------------
    # ambil 1 (pertama) dengan mempertimbangkan filter
    # -------------------------
    def __pertama__(self):
        try:
            base_sql = f"SELECT * FROM {self.table_name}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql + " LIMIT 1"

            self.cursor.execute(sql, params)

            if not self.cursor.description:
                self.where_clause, self.where_values, self._or_clauses = [], [], []
                # return {}
                return None

            kolom = [desc[0] for desc in self.cursor.description]
            baris = self.cursor.fetchone()

            self.where_clause, self.where_values, self._or_clauses = [], [], []

            if not baris:
                return None
            return self._safe_dict(kolom, baris)
        except Exception as e:
            self._last_error = str(e)
            return False

    # -------------------------
    # semua() — alias untuk ambil (konsisten dengan filter)
    # -------------------------
    def __semua__(self):
        # Memanfaatkan __ambil__ supaya logika filter konsisten
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
                return "[tarri | sqlite] Tidak ada data dalam tabel."
            kolom = list(data[0].keys())
            baris = [list(d.values()) for d in data]
            lebar = [max(len(str(k)), max(len(str(r[i])) for r in baris)) for i, k in enumerate(kolom)]

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
            return f"[tarri | sqlite] Gagal menampilkan tabel: {e}"

    # -------------------------
    # urutkan() dengan dukungan filter
    # -------------------------
    def __urutkan__(self, arah="a-z", kolom="id"):
        try:
            arah_sql = "ASC" if arah.lower() == "a-z" else "DESC"
            base_sql = f'SELECT * FROM "{self.table_name}"'
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql + f' ORDER BY "{kolom}" {arah_sql}'

            self.cursor.execute(sql, params)
            kolom = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
            baris = self.cursor.fetchall()

            # reset filter setelah digunakan
            self.where_clause, self.where_values, self._or_clauses = [], [], []

            return [self._safe_dict(kolom, b) for b in baris]
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal mengurutkan data: {e}")
            return False

    # -------------------------
    # delete (hapus) — sudah mendukung AND + OR
    # -------------------------
    def __hapus__(self):
        try:
            if not self.where_clause and not self._or_clauses:
                raise Exception("Gunakan 'dimana()' sebelum hapus()")

            base_sql = f"DELETE FROM {self.table_name}"
            where_sql, params = self._build_where_clause()
            sql = base_sql + where_sql

            self.cursor.execute(sql, params)
            self.conn.commit()

            # reset filter setelah digunakan
            self.where_clause, self.where_values, self._or_clauses = [], [], []

            if self.cursor.rowcount == 0:
                self.log(f"Tidak ada data yang cocok untuk dihapus dari tabel '{self.table_name}'.")
                return False

            self.log(f"Data dihapus dari tabel '{self.table_name}'.")
            return True
        except Exception as e:
            self._last_error = str(e)
            self.log(f"Gagal menghapus data: {e}")
            # pastikan reset agar tidak bocor state
            self.where_clause, self.where_values, self._or_clauses = [], [], []
            return False

    # -------------------------
    # filter helpers (dimana, danDimana, atauDimana)
    # -------------------------

    
    def __dimana__(self, kolom, nilai):
        kol_quoted = f'"{kolom}"' if not (kolom.startswith('"') and kolom.endswith('"')) else kolom

        if isinstance(nilai, str) and len(nilai) >= 3:
            # LIKE untuk minimal 3 huruf
            self.where_clause = [f'{kol_quoted} LIKE ?']
            self.where_values = [f'%{nilai}%']
            self.log(f"Dimana : {kolom} Seperti '%{nilai}%'")
        else:
            # exact match
            self.where_clause = [f'{kol_quoted} = ?']
            self.where_values = [nilai]
            self.log(f"Dimana Exact: {kolom} = {nilai}")

        return True



    def __danDimana__(self, kolom, nilai):
        kol_quoted = f'"{kolom}"' if not (kolom.startswith('"') and kolom.endswith('"')) else kolom

        if isinstance(nilai, str) and len(nilai) >= 3:
            # AND LIKE
            self.where_clause.append(f'{kol_quoted} LIKE ?')
            self.where_values.append(f'%{nilai}%')
            self.log(f"DanDimana : {kolom} Seperti '%{nilai}%'")
        else:
            # AND exact
            self.where_clause.append(f'{kol_quoted} = ?')
            self.where_values.append(nilai)
            self.log(f"DanDimana Exact: {kolom} = {nilai}")

        return True



    def __atauDimana__(self, kolom, nilai):
        if isinstance(nilai, str) and len(nilai) >= 3:
            clause = (kolom, 'LIKE', f'%{nilai}%')
            self.log(f"AtauDimana : {kolom} Seperti '%{nilai}%'")
        else:
            clause = (kolom, '=', nilai)
            self.log(f"AtauDimana Exact: {kolom} = {nilai}")

        self._or_clauses.append(clause)
        return True


# buat object
sqlite = SQLiteHandler()
tabel_sqlite = Tabel

# alias method agar bisa dipanggil langsung
sqlite.koneksi = sqlite.__koneksi__
sqlite.buat = sqlite.__buat__
sqlite.simpan = sqlite.__simpan__
sqlite.ubah = sqlite.__ubah__
sqlite.ambil = sqlite.__ambil__
sqlite.semua = sqlite.__semua__
sqlite.pertama = sqlite.__pertama__
sqlite.rapi = sqlite.__rapi__
sqlite.tabel = sqlite.__tabel__
sqlite.hapus = sqlite.__hapus__
sqlite.dimana = sqlite.__dimana__
sqlite.danDimana = sqlite.__danDimana__
sqlite.atauDimana = sqlite.__atauDimana__
sqlite.urutkan = sqlite.__urutkan__
