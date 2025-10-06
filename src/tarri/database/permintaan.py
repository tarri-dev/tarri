import sqlite3
from tarri.database.buattabel import BasisData, get_table_name
from tarri.database.buatbasisdata import get_db_path

def simpan(data_dict, bd_obj):
    try:
        db_path = get_db_path()
        nama_tabel = get_table_name()

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Ambil nama kolom dari tabel, kecuali kolom auto
        cur.execute(f'PRAGMA table_info("{nama_tabel}")')
        kolom_info = cur.fetchall()
        kolom_nama = [row[1] for row in kolom_info if row[1] not in ("id", "dibuat", "diubah")]

        # Validasi: pastikan semua key di data_dict adalah kolom yang sah
        for k in data_dict.keys():
            if k not in kolom_nama:
                raise ValueError(f"Kolom tidak dikenal: {k}")

        # Identifikasi kolom pilihan yang harus lowercase
        kolom_choice = []
        if hasattr(bd_obj, "columns"):
            for col_def in bd_obj.columns:
                if "CHECK" in col_def and "LOWER" in col_def:
                    nama_col = col_def.split()[0]
                    kolom_choice.append(nama_col)

        # Siapkan data
        kolom_final = []
        nilai_final = []
        for k in data_dict:
            kolom_final.append(f'"{k}"')
            v = data_dict[k]
            if k in kolom_choice and isinstance(v, str):
                nilai_final.append(v.lower())
            else:
                nilai_final.append(v)

        kolom_str = ", ".join(kolom_final)
        placeholder = ", ".join(["?"] * len(nilai_final))
        sql = f'INSERT INTO "{nama_tabel}" ({kolom_str}) VALUES ({placeholder})'

        try:
            cur.execute(sql, tuple(nilai_final))
            conn.commit()
            return "sukses"
        except sqlite3.IntegrityError:
            return (
                "Gagal menyimpan data: nilai salah untuk kolom pilihan.\n"
                "Periksa opsi yang tersedia dan pastikan ejaannya benar.\n"
                "Huruf besar/kecil akan otomatis disimpan huruf kecil."
            )
        finally:
            conn.close()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Gagal menyimpan data: {e}"





# Variabel global untuk menyimpan objek aktif
_objek_aktif = None

class Ambil:
    def __init__(self, db_path, table_name):
        self._pilih_kolom = ["*"]

        if not table_name:
            raise ValueError("[ERROR Ambil] table_name tidak ditemukan")
        if not db_path:
            raise ValueError("[ERROR Ambil] db_path tidak ditemukan")

        self.db_path = db_path
        self.table_name = table_name
        self._wheres = []
        self._cache = None
        self._limit = None
        
    # def pilih(self, *kolom):
    #     self._pilih_kolom = list(kolom) if kolom else ["*"]
    #     self._cache = None
    #     self._render_cache = {}
    #     return self
    
    def pilih(self, *kolom):
        if kolom:
            self._pilih_kolom = list(kolom)  # kolom spesifik
        else:
            self._pilih_kolom = None         # None artinya semua kolom (*)
        self._cache = None
        self._render_cache = {}
        return self

    
    def batasi(self, jumlah):
        self._limit = int(jumlah)
        self._cache = None
        self._render_cache = {}
        return self


    def dimana(self, kolom, nilai):
        self._wheres.append(("AND", kolom, nilai))
        self._cache = None
        self._render_cache = {}
        return self

    def atau_dimana(self, kolom, nilai):
        self._wheres.append(("OR", kolom, nilai))
        self._cache = None
        self._render_cache = {}
        return self
    
    def dan_dimana(self, kolom, nilai):
        self._wheres.append(("AND", kolom, nilai))
        self._cache = None
        self._render_cache = {}
        return self

    def _build_where_clause(self):
        if not self._wheres:
            return "", []
        clauses = []
        params = []
        for i, (op, k, v) in enumerate(self._wheres):
            prefix = op if i > 0 else ""
            clauses.append(f"{prefix} \"{k}\" = ?")
            params.append(v)
        return " WHERE " + " ".join(clauses), params

    def semua(self):
        if self._cache is not None:
            return self._cache

        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 🔧 perbaikan di sini
        if not self._pilih_kolom or self._pilih_kolom == ["*"]:
            kolom_sql = "*"  # ambil semua kolom
        else:
            # bungkus kolom dengan quote biar aman dari reserved keyword
            kolom_sql = ", ".join(f'"{k}"' for k in self._pilih_kolom)

        sql = f'SELECT {kolom_sql} FROM "{self.table_name}"'

        where_sql, params = self._build_where_clause()
        sql += where_sql
        
        # 🔧 Tambahkan ORDER BY
        if hasattr(self, "_order_by") and self._order_by:
            kolom, arah = self._order_by
            sql += f' ORDER BY "{kolom}" {arah}'

        if self._limit:
            sql += f" LIMIT {self._limit}"

        cur.execute(sql, params)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        # ubah Row → dict agar lebih enak diakses
        self._cache = [dict(r) for r in rows]
        return self._cache



    # def pertama(self):
    #     self._limit = 1
    #     self._cache = None
    #     self._render_cache = {}
    #     hasil = self.semua()
    #     return hasil[0] if hasil else None
    
    def pertama(self):
        self._limit = 1
        self._cache = None
        self._render_cache = {}
        hasil = self.semua()
        self._render_cache[("json", 2)] = hasil[0]  # opsional
        return hasil[0] if hasil else None

    def urutkan(self, mode: str):
        mapping = {
            "awal-akhir":  ('id', 'ASC'),
            "akhir-awal":  ('id', 'DESC'),
            "kecil-besar": ('nilai', 'ASC'),
            "besar-kecil": ('nilai', 'DESC'),
        }

        if mode not in mapping:
            raise ValueError(f"Mode urutkan tidak dikenal: {mode}")

        kolom, arah = mapping[mode]
        self._order_by = (kolom, arah)
        self._cache = None
        self._render_cache = {}
        return self

    
    
    def rapi(self, mode="json", indent=2):
    # Buat key cache berdasarkan mode dan indent
        key = (mode, indent)

        # Cek apakah hasil sudah ada di cache
        if hasattr(self, "_render_cache") and key in self._render_cache:
            return self._render_cache[key]

        hasil = self.semua()
        if not hasil:
            return "gagal"

        if mode == "json":
            import json
            output = json.dumps(hasil, indent=indent, ensure_ascii=False)

        elif mode == "tabel":
            headers = list(hasil[0].keys())
            col_widths = [max(len(str(row[h])) for row in hasil + [{h:h}]) for h in headers]
            header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
            separator = "-" * len(header_line)
            lines = [header_line, separator]
            for row in hasil:
                line = " | ".join(str(row[h]).ljust(w) for h, w in zip(headers, col_widths))
                lines.append(line)
            output = "\n".join(lines)

        elif mode == "csv":
            import io
            import csv
            output_io = io.StringIO()
            writer = csv.DictWriter(output_io, fieldnames=hasil[0].keys())
            writer.writeheader()
            writer.writerows(hasil)
            output = output_io.getvalue()

        elif mode == "html":
            import webbrowser
            import os

            headers = list(hasil[0].keys())
            header_html = "".join(f"<th>{h}</th>" for h in headers)

            rows_html = ""
            for row in hasil:
                baris = ""
                for h in headers:
                    nilai = row[h]
                    if h == "nama":
                        link = nilai.lower().replace(" ", "_") + ".html"
                        baris += f'<td><a href="{link}">{nilai}</a></td>'
                    else:
                        baris += f"<td>{nilai}</td>"
                rows_html += f"<tr>{baris}</tr>"

            output = f"""
            <!DOCTYPE html>
            <html lang="id">
            <head>
                <meta charset="UTF-8">
                <title>Data Siswa</title>
                <style>
                    body {{ font-family: sans-serif; padding: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    a {{ color: #007acc; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <h2>Data Siswa</h2>
                <table>
                    <thead><tr>{header_html}</tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </body>
            </html>
            """

            try:
                nama_file = "_ambil_data.html"
                with open(nama_file, "w", encoding="utf-8") as f:
                    f.write(output)
                webbrowser.open(nama_file)
                BLUE_UNDERLINE = "\033[34;4m"
                RESET = "\033[0m"
                path = os.path.abspath(nama_file)
                output = f"File HTML sudah dibuat. Klik di sini untuk membuka file:\n{BLUE_UNDERLINE}{path}{RESET}"
            except Exception as e:
                output = f"Gagal menyimpan HTML: {e}"

        else:
            output = f"Mode '{mode}' tidak dikenali"

        # Simpan ke cache
        if not hasattr(self, "_render_cache"):
            self._render_cache = {}
        self._render_cache[key] = output
        return output



class Ubah:
    def __init__(self, db_path, table_name, data_baru):
        self.db_path = db_path
        self.table_name = table_name
        self.data_baru = data_baru
        self._wheres = []

    def dimana(self, kolom, nilai):
        self._wheres.append((kolom, nilai))
        return self._eksekusi()

    def _eksekusi(self):
        if not self.data_baru or not isinstance(self.data_baru, dict):
            return "gagal"

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Ambil nama kolom dari tabel, kecuali kolom auto
            cur.execute(f'PRAGMA table_info("{self.table_name}")')
            kolom_info = cur.fetchall()
            kolom_sah = [row[1] for row in kolom_info if row[1] not in ("id", "dibuat", "diubah")]

            # Filter kolom yang akan diubah (skip jika kosong atau bukan kolom sah)
            kolom_ubah = []
            nilai_ubah = []
            for k, v in self.data_baru.items():
                if k not in kolom_sah:
                    continue  # abaikan kolom tidak sah
                if isinstance(v, str) and v.strip() == "":
                    continue  # abaikan nilai kosong
                kolom_ubah.append(k)
                nilai_ubah.append(v)

            if not kolom_ubah:
                return "gagal: tidak ada data yang diubah"

            set_clause = ", ".join([f'"{k}" = ?' for k in kolom_ubah])
            where_clause = " AND ".join([f'"{k}" = ?' for k, _ in self._wheres])
            where_params = [v for _, v in self._wheres]

            sql = f'UPDATE "{self.table_name}" SET {set_clause} WHERE {where_clause}'
            cur.execute(sql, nilai_ubah + where_params)
            conn.commit()
            conn.close()
            return "sukses"

        except Exception as e:
            return f"gagal: {e}"



class Hapus:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self._wheres = []

    def dimana(self, kolom, nilai):
        self._wheres.append((kolom, nilai))
        return self._eksekusi()

    def _eksekusi(self):
        if not self._wheres:
            return "gagal: kondisi WHERE tidak diberikan"

        where_clause = " AND ".join([f'"{k}" = ?' for k, _ in self._wheres])
        where_params = [v for _, v in self._wheres]
        sql_check = f'SELECT COUNT(*) FROM "{self.table_name}" WHERE {where_clause}'
        sql_delete = f'DELETE FROM "{self.table_name}" WHERE {where_clause}'

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(sql_check, where_params)
            count = cur.fetchone()[0]
            if count == 0:
                kondisi = " dan ".join([f'{k} = "{v}"' for k, v in self._wheres])
                conn.close()
                return f'gagal: {kondisi} tidak ditemukan'

            cur.execute(sql_delete, where_params)
            conn.commit()
            conn.close()
            return "sukses"

        except Exception as e:
            kondisi = " dan ".join([f'{k} = "{v}"' for k, v in self._wheres])
            return f'gagal: {kondisi} ({e})'



# Fungsi global utama Tarri
def ambil(bd_lokasi, bd_nama, tabel_nama):
    global _objek_aktif
    _objek_aktif = Ambil(f"{bd_lokasi}/{bd_nama}", tabel_nama)
    return _objek_aktif

def ubah(bd_lokasi, bd_nama, tabel_nama, data_baru):
    global _objek_aktif
    _objek_aktif = Ubah(f"{bd_lokasi}/{bd_nama}", tabel_nama, data_baru)
    return _objek_aktif

def hapus(bd_lokasi, bd_nama, tabel_nama, _):
    global _objek_aktif
    _objek_aktif = Hapus(f"{bd_lokasi}/{bd_nama}", tabel_nama)
    return _objek_aktif

def semua():
    global _objek_aktif
    return _objek_aktif.semua()

def atau_dimana(kolom, nilai):
    global _objek_aktif
    _objek_aktif = _objek_aktif.atau_dimana(kolom, nilai)
    return _objek_aktif

def dan_dimana(kolom, nilai):
    global _objek_aktif
    _objek_aktif = _objek_aktif.dan_dimana(kolom, nilai)
    return _objek_aktif

def rapi(*args):
    global _objek_aktif
    mode = args[0] if len(args) >= 1 else "json"
    indent = int(args[1]) if len(args) >= 2 else 2
    return _objek_aktif.rapi(mode=mode, indent=indent)

def dimana(kolom, nilai):
    global _objek_aktif

    if isinstance(_objek_aktif, Ambil):
        _objek_aktif = _objek_aktif.dimana(kolom, nilai)
        return _objek_aktif

    elif isinstance(_objek_aktif, Hapus):
        _objek_aktif._wheres.append((kolom, nilai))
        return _objek_aktif._eksekusi()

    elif isinstance(_objek_aktif, Ubah):
        _objek_aktif._wheres.append((kolom, nilai))
        return _objek_aktif._eksekusi()

    else:
        return "gagal: objek aktif tidak dikenali"

def batasi(jumlah):
    global _objek_aktif
    _objek_aktif = _objek_aktif.batasi(jumlah)
    return _objek_aktif

def pertama():
    global _objek_aktif
    return _objek_aktif.pertama()


def pilih(*kolom):
    global _objek_aktif
    _objek_aktif = _objek_aktif.pilih(*kolom)
    return _objek_aktif



def urutkan(mode):
    global _objek_aktif
    pilihan_valid = ["awal-akhir", "akhir-awal", "kecil-besar", "besar-kecil"]

    if mode not in pilihan_valid:
        import sys
        print(f"\033[91m[tarri | permintaan] kesalahan: mode urutkan '{mode}' tidak valid\033[0m", file=sys.stderr, flush=True)
        print(f"\033[91m[tarri | permintaan] Gunakan salah satu dari: {', '.join(pilihan_valid)}\033[0m", file=sys.stderr, flush=True)
        return _objek_aktif  # tetap kembalikan objek biar chain gak rusak

    _objek_aktif = _objek_aktif.urutkan(mode)
    return _objek_aktif

