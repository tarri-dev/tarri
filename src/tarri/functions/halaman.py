from pathlib import Path
import re
import datetime
from tarri.parser_global import parser
from tarri.functions.tujuan import tujuan
from tarri.functions.rute import ROUTES
from fastapi.responses import RedirectResponse, HTMLResponse
from tarri.functions.alihkan import alihkan
import io
import contextlib
import subprocess


_DOUBLE_PATTERN = re.compile(r"{{([^{}]+)}}")
_RAW_PATTERN   = re.compile(r"{!!([^{}]+)!!}")  # pattern untuk raw HTML

def render_html(html, context):
    def repl(match):
        """Render {{ variable }} seperti sebelumnya"""
        expr = match.group(1).strip()

        # ===============================
        # Fungsi Tarri: contoh tujuan("/")
        # ===============================
        if "(" in expr and expr.endswith(")"):
            func_name = expr.split("(")[0].strip()
            args_raw = expr[len(func_name)+1:-1].strip()  # ambil isi dalam ()
            args = []

            if args_raw:
                # anggap argumen string ("" atau '') atau angka
                for a in args_raw.split(","):
                    a = a.strip()
                    if (a.startswith('"') and a.endswith('"')) or (a.startswith("'") and a.endswith("'")):
                        args.append(a[1:-1])
                    else:
                        try:
                            args.append(int(a))
                        except ValueError:
                            args.append(a)

            if func_name in context and callable(context[func_name]):
                try:
                    return str(context[func_name](*args))
                except Exception as e:
                    return f"[error fungsi {func_name}: {e}]"
            else:
                return f"[fungsi '{func_name}' tidak ditemukan]"

        # ===============================
        # Akses dict dengan ["key"]
        # ===============================
        elif '["' in expr and expr.endswith('"]'):
            parts = expr.split('["')
            val = context
            for p in parts:
                p = p.rstrip('"]')
                if isinstance(val, dict):
                    val = val.get(p, f"[key '{p}' tidak ditemukan]")
                else:
                    val = getattr(val, p, f"[attr '{p}' tidak ditemukan]")
            return str(val)

        # ===============================
        # fallback: akses dict/atribut biasa
        # ===============================
        keys = expr.split(".")
        val = context
        try:
            for k in keys:
                if isinstance(val, dict):
                    val = val.get(k, f"[key '{k}' tidak ditemukan]")
                else:
                    val = getattr(val, k, f"[attr '{k}' tidak ditemukan]")
            return str(val)
        except Exception:
            return match.group(0)

    def repl_raw(match):
        """Render {!! variable !!} → raw HTML"""
        expr = match.group(1).strip()

        # logika sama seperti repl tapi tidak mengubah string → raw
        if "(" in expr and expr.endswith(")"):
            func_name = expr.split("(")[0].strip()
            args_raw = expr[len(func_name)+1:-1].strip()
            args = []
            if args_raw:
                for a in args_raw.split(","):
                    a = a.strip()
                    if (a.startswith('"') and a.endswith('"')) or (a.startswith("'") and a.endswith("'")):
                        args.append(a[1:-1])
                    else:
                        try:
                            args.append(int(a))
                        except ValueError:
                            args.append(a)
            if func_name in context and callable(context[func_name]):
                try:
                    return str(context[func_name](*args))
                except Exception as e:
                    return f"[error fungsi {func_name}: {e}]"
            else:
                return f"[fungsi '{func_name}' tidak ditemukan]"

        elif '["' in expr and expr.endswith('"]'):
            parts = expr.split('["')
            val = context
            for p in parts:
                p = p.rstrip('"]')
                if isinstance(val, dict):
                    val = val.get(p, f"[key '{p}' tidak ditemukan]")
                else:
                    val = getattr(val, p, f"[attr '{p}' tidak ditemukan]")
            return str(val)

        keys = expr.split(".")
        val = context
        try:
            for k in keys:
                if isinstance(val, dict):
                    val = val.get(k, f"[key '{k}' tidak ditemukan]")
                else:
                    val = getattr(val, k, f"[attr '{k}' tidak ditemukan]")
            return str(val)
        except Exception:
            return match.group(0)

    # render {!! !!} dulu → raw HTML
    html = _RAW_PATTERN.sub(repl_raw, html)
    # render {{ }} setelahnya → aman
    html = _DOUBLE_PATTERN.sub(repl, html)
    return html

def get_tarri_version():
    try:
        result = subprocess.run(
            ["tarri", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return "[tarri | server] Versi tidak ditemukan"
    
def render_error_page(code=404, message="Halaman tidak ditemukan", path="/"):
    return f"""
    <html><head><meta charset="utf-8"><title>Error {code} • TarriWeb</title></head>
    <body style="font-family:sans-serif;text-align:center;margin-top:15%">
        <h1>{code}</h1><p>{message}</p><code>{path}</code>
        <p style="font-size:12px;color:#777">TarriWeb • {get_tarri_version()}</p>
    </body></html>
    """

def halaman(interpreter, args, fungsi=None):
    """
    Eksekusi halaman:
    - Jika .tarri.html → jalankan <tarri> block + render template {{var}}
    - Jika .tarri → jalankan seluruh file sebagai kode TARRI
    - POST → jalankan fungsi target jika ada
    """
    if not args:
        return HTMLResponse("<p style='color:red;'>[halaman] ERROR: Tidak ada argumen yang diberikan</p>", status_code=400)
    

    raw_path = str(args[0])
    file_path = Path(raw_path).resolve()
    context = {}
    
    if len(args) > 1:
        payload = args[1]
        if isinstance(payload, dict):
            # jika nilai UploadFile atau field, ambil .value atau .read()
            clean_payload = {}
            for k, v in payload.items():
                if hasattr(v, "read"):  # file-like
                    clean_payload[k] = v.read().decode('utf-8')
                else:
                    clean_payload[k] = v
            context = clean_payload
        else:
            context = {"_data": payload}

    
    default_context = {
        "_url": str(file_path),
        "_method": context.get("_method", "GET"),
        "_now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "_no_cache": True,
        "tujuan": tujuan,
        "alihkan": lambda path, data=None: alihkan(interpreter, path, data),
        "_redirect": None,
    }

    context = {**default_context, **context}
    interpreter.context.update(context)
    
    if not file_path.exists():
        html = render_error_page(
            404,
            f"File <b>{file_path.name}</b> tidak ditemukan!",
            str(file_path)
        )
        return HTMLResponse(html, status_code=404)


    source = file_path.read_text(encoding="utf-8")

    if file_path.suffix.lower() == ".tarri":
        try:
            tree = parser.parse(source)
            interpreter.run(tree)
        except Exception as e:
            if context["_method"].upper() == "POST":
                return HTMLResponse(f"<p>{e}</p>", status_code=500)
            context["_halaman_error"] = f"<p>{e}</p>"
        rendered_html = "" 
    else:
        tarri_block_pattern = re.compile(r"<tarri>(.*?)</tarri>", re.DOTALL)
        blocks = tarri_block_pattern.findall(source)
        for block in blocks:
            try:
                tree = parser.parse(block)
                interpreter.run(tree)
            except Exception as e:
                import traceback
                err_msg = str(e) or traceback.format_exc()
                if context["_method"].upper() == "POST":
                    return HTMLResponse(f"<p>{err_msg}</p>", status_code=500)
                context["_halaman_error"] = f"<p>{err_msg}</p>"


        context.update(interpreter.context)
        source = tarri_block_pattern.sub("", source)
        if "_halaman_error" in context and context["_method"].upper() == "GET":
            source = context["_halaman_error"] + source
        rendered_html = render_html(source, context)
    
    
    # if context["_method"].upper() == "POST" and fungsi:
    #     if fungsi in interpreter.functions:
    #         result = interpreter.call_function(fungsi, [])
    if context["_method"].upper() == "POST" and fungsi:
        if fungsi in interpreter.functions:
            # Ambil semua parameter route dari context
            route_kwargs = interpreter.context.get("_rute_kwargs", {})

            # Debug bantu
            # print("[DEBUG CALL TARII FUNKSI]", fungsi, "ARGS:", route_kwargs)

            # Panggil fungsi dengan parameter sesuai route
            if route_kwargs:
                result = interpreter.call_function(fungsi, list(route_kwargs.values()))
            else:
                result = interpreter.call_function(fungsi, [])

            if isinstance(result, HTMLResponse):
                return result 
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                if result is not None:
                    buf.write(str(result))
            output = buf.getvalue()
            return HTMLResponse(output)
        else:
            css = """
            <style>
            .tarri-dump-container {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                margin: 15px 0;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                overflow: hidden;
                margin-left:auto;
                margin-right:auto;
            }
            .dump-header {
                background: #f8fafc;
                padding: 14px 18px;
                border-bottom: 1px solid #e2e8f0;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .dump-title {
                font-weight: 600;
                color: #2d3748;
                font-size: 17px;
            }
            .dump-type-badge {
                background: #fed7d7;
                color: #9b2c2c;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
            }
            .dump-content {
                padding: 20px;
                background: #fff;
            }
            .dump-value {
                background: #fff5f5;
                padding: 14px;
                border-radius: 6px;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                font-size: 14px;
                line-height: 1.6;
                color: #c53030;
                white-space: pre-wrap;
                overflow-x: auto;
                border: 1px solid #feb2b2;
            }
            .dump-info {
                margin-top: 14px;
                padding: 10px 14px;
                background: #ebf8ff;
                border-radius: 6px;
                border-left: 3px solid #4299e1;
                font-size: 13px;
                color: #2b6cb0;
            }
            .center {
                text-align: center;
            }
            .footer {
                margin-top: 16px;
                padding: 12px;
                color: #718096;
                font-size: 12px;
                border-top: 1px solid #e2e8f0;
            }
            </style>
            """

            output_html = f"""
            {css}
            <div class="tarri-dump-container">
                <div class="dump-header">
                    <div class="dump-title">Kesalahan Saat Eksekusi</div>
                    <div class="dump-type-badge">Fungsi Tidak Ditemukan</div>
                </div>
                <div class="dump-content">
                    <div class="dump-value">⚠️ Fungsi "<strong>{fungsi}</strong>" tidak ditemukan di file <b>{file_path.name}</b>.</div>
                    <div class="dump-info">
                        <strong>💡 Solusi:</strong> Pastikan fungsi tersebut didefinisikan di dalam file 
                        <code>{file_path.name}</code> atau periksa ejaan nama fungsinya di <code>rute.tarri</code>.
                    </div>
                    
                    <div class="footer center">
                        TarriWeb • Proses dihentikan otomatis
                    </div>
                </div>
            </div>
            """
            return HTMLResponse(output_html, status_code=500)

    return HTMLResponse(rendered_html)
