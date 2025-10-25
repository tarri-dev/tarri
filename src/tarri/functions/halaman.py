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
    # if hasattr(interpreter, "redirect") and callable(interpreter.redirect):
    #     if hasattr(interpreter, "session"):
    #         interpreter.session["redirect_data"] = context
    #         print("[tarri | halaman] halaman() redirect_data:", context)
    #         return interpreter.redirect(file_path, context)
    #     else:
    #         return "[halaman] ERROR: Interpreter tidak mendukung session"
    # else:
    #     return "[halaman] ERROR: Interpreter tidak mendukung redirect"
    
    if hasattr(interpreter, "session"):
        interpreter.session["redirect_data"] = context
        try:
            import tarri.parser_global as pg
            if hasattr(pg, "global_ctx"):
                sesi_obj = pg.global_ctx.get("sesi")
                if sesi_obj is not None:
                    setattr(sesi_obj, "redirect_data", context)
                    print("[tarri | halaman] sinkron ke parser_global.global_ctx.sesi.redirect_data:", context)
        except Exception as e:
            print("[tarri | halaman] gagal sinkron sesi:", e)
        return interpreter.redirect(file_path, context)
