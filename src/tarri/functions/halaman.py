# halaman.py
from pathlib import Path
import re
import datetime
from tarri.parser_global import get_env
# from tarriweb import server

# Cache compiled regex untuk performa lebih baik
_TEMPLATE_PATTERN = re.compile(r"{([^{}]+)}")

def render_html(html, context):
    """
    Render template HTML dengan mengganti placeholder {variabel} 
    dengan nilai dari context dictionary.
    Support nested data (misal {user.name} atau {angka.0})
    """
    def repl(match):
        key = match.group(1).strip()
        keys = key.split(".")
        value = context
        try:
            for k in keys:
                # index array kalau k angka
                if isinstance(value, (list, tuple)) and k.isdigit():
                    value = value[int(k)]
                else:
                    value = value[k]
            return str(value)
        except (KeyError, TypeError, IndexError):
            return match.group(0)  # kalau gagal, biarkan placeholder asli

    return _TEMPLATE_PATTERN.sub(repl, html)


def halaman(interpreter, args):
    """
    Fungsi redirect ke halaman tertentu dengan membawa context dinamis.
    - args[0]: path tujuan (misal "/")
    - args[1]: pesan (string atau dict)
    - args[2]: opsional nama variabel (default "_sukses")
    """
    if not args:
        return "[halaman] ERROR: Tidak ada argumen yang diberikan"

    file_path = str(args[0])
    print("[tarri | halaman] halaman() redirect ke:", file_path)

    # Tentukan nama variabel pesan
    nama_var = "_sukses"
    if len(args) > 2 and isinstance(args[2], str):
        nama_var = args[2]

    # Bangun data pesan
    if len(args) > 1:
        if isinstance(args[1], dict):
            data = args[1]
        else:
            data = {nama_var: str(args[1])}
    else:
        data = {}

    # Konteks default redirect
    default_context = {
        "_url": file_path,
        "_method": "GET",
        "_now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "_no_cache": True
    }

    # Gabungkan semua
    context = {**default_context, **data}
    interpreter._last_context = context

    # Simpan ke session dan redirect
    if hasattr(interpreter, "redirect") and callable(interpreter.redirect):
        if hasattr(interpreter, "session"):
            interpreter.session["redirect_data"] = context
            print("[tarri | halaman] halaman() redirect_data:", context)
            return interpreter.redirect(file_path, context)
        else:
            return "[halaman] ERROR: Interpreter tidak mendukung session"
    else:
        return "[halaman] ERROR: Interpreter tidak mendukung redirect"



# def halaman(interpreter, args):
#     if not args:
#         return "[halaman] ERROR: Tidak ada argumen yang diberikan"

#     file_path = str(args[0])
#     print("Redirect ke:", file_path)

#     data = {}
#     if len(args) > 1:
#         if isinstance(args[1], dict):
#             data = args[1]
#         else:
#             data = {"_gagal": str(args[1])}

#     default_context = {
#         "_url": file_path,
#         "_method": "GET",
#         "_now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "_no_cache": True  # ← tambahkan flag ini
#     }

#     context = {**default_context, **data}

#     interpreter._last_context = context

#     if hasattr(interpreter, "redirect") and callable(interpreter.redirect):
#         if hasattr(interpreter, "session"):
#             interpreter.session["redirect_data"] = context
#             return interpreter.redirect(file_path, context)
#         else:
#             return "[halaman] ERROR: Interpreter tidak mendukung redirect"



# def halaman(interpreter, args):
#     """
#     Fungsi redirect halaman dengan membawa variabel.
#     Penggunaan:
#         tampilkan halaman("/login", "Email salah")
#         tampilkan halaman("/home", {"_sukses": "Berhasil login"})
#         tampilkan halaman("/profile", {"user": {"nama": "Ketut"}, "angka": [1,2,3]})
#     """
#     if not args:
#         return "[halaman] ERROR: Tidak ada argumen yang diberikan"

#     # Ambil path tujuan
#     file_path = str(args[0])
#     print("Redirect ke:", file_path)

#     # Proses data input
#     data = {}
#     if len(args) > 1:
#         if isinstance(args[1], dict):
#             data = args[1]
#         else:
#             # default string → anggap gagal
#             data = {"_gagal": str(args[1])}

#     # Tambahkan data default
#     default_context = {
#         "_url": file_path,
#         "_method": "GET",
#         "_now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

#     # Gabungkan data default dengan data user (tanpa flatten)
#     context = {**default_context, **data}

#     # Simpan agar bisa diakses lagi (opsional)
#     interpreter._last_context = context
    
#     if hasattr(interpreter, "redirect") and callable(interpreter.redirect):
#     # simpan context di session agar tangani_output bisa membaca
#         if hasattr(interpreter, "session"):
#             interpreter.session["redirect_data"] = context
#             return interpreter.redirect(file_path, context)
#         else:
#             return "[halaman] ERROR: Interpreter tidak mendukung redirect"
