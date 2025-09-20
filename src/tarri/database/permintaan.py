import sqlite3
from tarri.database.buattabel import BasisData, get_table_name
from tarri.database.buatbasisdata import get_db_path

def simpan(data_list, bd_obj):

    try:
        db_path = get_db_path()
        nama_tabel = get_table_name()

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ambil nama kolom dari tabel, kecuali kolom auto
        cur.execute(f'PRAGMA table_info("{nama_tabel}")')
        kolom_info = cur.fetchall()
        kolom_nama = [row[1] for row in kolom_info if row[1] not in ("id", "dibuat", "diubah")]

        if len(data_list) != len(kolom_nama):
            raise ValueError("Jumlah elemen list tidak sesuai jumlah kolom")

        # **Simpan semua kolom pilihan TEXT dengan constraint LOWER menjadi lowercase**
        # Kita anggap semua kolom TEXT dengan nama kolom di bd_obj.columns yang mengandung 'CHECK' adalah pilihan
        kolom_choice = []
        if hasattr(bd_obj, "columns"):
            for col_def in bd_obj.columns:
                if "CHECK" in col_def and "LOWER" in col_def:
                    nama_col = col_def.split()[0]
                    kolom_choice.append(nama_col)

        data_prepared = []
        for col, val in zip(kolom_nama, data_list):
            if col in kolom_choice and isinstance(val, str):
                data_prepared.append(val.lower())  # simpan lowercase
            else:
                data_prepared.append(val)

        kolom_quoted = ", ".join([f'"{c}"' for c in kolom_nama])
        placeholder = ", ".join(["?"] * len(data_prepared))
        sql = f'INSERT INTO "{nama_tabel}" ({kolom_quoted}) VALUES ({placeholder})'

        try:
            cur.execute(sql, tuple(data_prepared))
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
        if not table_name:
            raise ValueError("[ERROR Ambil] table_name tidak ditemukan")
        if not db_path:
            raise ValueError("[ERROR Ambil] db_path tidak ditemukan")

        self.db_path = db_path
        self.table_name = table_name
        self._wheres = []

    def dimana(self, kolom, nilai):
        self._wheres.append(("AND", kolom, nilai))
        return self

    def atau_dimana(self, kolom, nilai):
        self._wheres.append(("OR", kolom, nilai))
        return self
    
    def dan_dimana(self, kolom, nilai):
        self._wheres.append(("AND", kolom, nilai))
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
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = f'SELECT * FROM "{self.table_name}"'
        where_sql, params = self._build_where_clause()
        sql += where_sql
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    def rapi(self, mode="json", indent=2):
        hasil = self.semua()
        if not hasil:
            return "gagal"

        if mode == "json":
            import json
            return json.dumps(hasil, indent=indent, ensure_ascii=False)

        elif mode == "tabel":
            headers = list(hasil[0].keys())
            col_widths = [max(len(str(row[h])) for row in hasil + [{h:h}]) for h in headers]
            header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
            separator = "-" * len(header_line)
            lines = [header_line, separator]
            for row in hasil:
                line = " | ".join(str(row[h]).ljust(w) for h, w in zip(headers, col_widths))
                lines.append(line)
            return "\n".join(lines)

        elif mode == "csv":
            import io
            import csv
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=hasil[0].keys())
            writer.writeheader()
            writer.writerows(hasil)
            return output.getvalue()

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
                        # nama jadi link ke halaman detail
                        link = nilai.lower().replace(" ", "_") + ".html"
                        baris += f'<td><a href="{link}">{nilai}</a></td>'
                    else:
                        baris += f"<td>{nilai}</td>"
                rows_html += f"<tr>{baris}</tr>"

            html_content = f"""
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
                    f.write(html_content)
                webbrowser.open(nama_file)
                BLUE_UNDERLINE = "\033[34;4m"
                RESET = "\033[0m"

                path = os.path.abspath(nama_file)
                return f"File HTML sudah dibuat. Klik di sini untuk membuka file:\n{BLUE_UNDERLINE}{path}{RESET}"

            except Exception as e:
                return f"Gagal menyimpan HTML: {e}"


        return f"Mode '{mode}' tidak dikenali"



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
        if not self.data_baru:
            return "gagal"

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            # Ambil nama kolom dari tabel, kecuali kolom auto
            cur.execute(f'PRAGMA table_info("{self.table_name}")')
            kolom_info = cur.fetchall()
            kolom_nama = [row[1] for row in kolom_info if row[1] not in ("id", "dibuat", "diubah")]

            if len(self.data_baru) != len(kolom_nama):
                return "gagal: jumlah data tidak cocok dengan jumlah kolom"

            # Filter kolom yang akan diubah (skip jika "")
            kolom_ubah = []
            nilai_ubah = []
            for k, v in zip(kolom_nama, self.data_baru):
                if isinstance(v, str) and v.strip() == "":
                    continue  # abaikan kolom kosong
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




# Fungsi utama Tarri
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




