from tarri.parser_global import parser
from urllib.parse import parse_qs
from io import StringIO
import contextlib
import subprocess
import datetime
import html


class BuiltinFunction:
    """Wrapper supaya fungsi Python bisa dipanggil oleh interpreter."""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        try:
            if len(args) == 1 and isinstance(args[0], list):
                args = args[0]
            return self.func(*args)
        except AttributeError:
            return self.func(*args)


# --- Builtins dasar ---
base_builtins = {
    "cetak": lambda *args: print(*args),
    "tampilkan": lambda f: f(),
    "masukkan": lambda prompt="": input(prompt) if prompt else input(),
}


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
        return "[tarri | cetak_henti] Versi tidak ditemukan"


def inject_request(interpreter, request_data):
    """Tambahkan fungsi get(), post(), request() ke interpreter"""
    def _get(key=None, default=""):
        if key is None:
            return request_data["_GET"]
        return request_data["_GET"].get(key, default)

    def _post(key=None, default=""):
        if key is None:
            return request_data["_POST"]
        return request_data["_POST"].get(key, default)

    def _request(key=None, default=""):
        if key is None:
            return request_data["_REQUEST"]
        return request_data["_REQUEST"].get(key, default)

    builtins = {
        "get": BuiltinFunction(_get),
        "post": BuiltinFunction(_post),
        "request": BuiltinFunction(_request),
    }

    for name, func in builtins.items():
        interpreter.globals[name] = func
        interpreter.functions[name] = ([], func)


def run_source(source: str, request_data=None):
    """
    Jalankan kode TARRI dan kembalikan:
    - output  : string hasil cetak (HTML safe)
    - context : dict variabel global
    """
    # ⬅️ Lazy import → putus circular import
    # from tarri.interpreter import Interpreter  
    from tarri.interpreter.core import Context

    interpreter = Context()

    # Masukkan builtins dasar
    for name, func in base_builtins.items():
        bf = BuiltinFunction(func)
        interpreter.globals[name] = bf
        interpreter.functions[name] = ([], bf)

    if request_data:
        inject_request(interpreter, request_data)

    output_buffer = StringIO()
    try:
        tree = parser.parse(source)
        with contextlib.redirect_stdout(output_buffer):
            interpreter.run(tree)

        html_output = output_buffer.getvalue().strip()

        ctx = {
            k: v
            for k, v in interpreter.globals.items()
            if not callable(v)
        }
        return html_output, ctx

    except StopIteration:
        html_output = output_buffer.getvalue().strip()
        return html_output, {}

    except Exception as e:
        import traceback, sys

        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_list = traceback.format_exception(exc_type, exc_value, exc_tb)
        formatted_traceback = "".join(tb_list)

        error_translations = {
            'SyntaxError': 'Kesalahan Sintaks',
            'NameError': 'Kesalahan Nama',
            'TypeError': 'Kesalahan Tipe Data',
            'ValueError': 'Kesalahan Nilai',
            'IndexError': 'Kesalahan Indeks',
            'KeyError': 'Kesalahan Kunci',
            'ZeroDivisionError': 'Kesalahan Pembagian dengan Nol',
            'ImportError': 'Kesalahan Import',
            'AttributeError': 'Kesalahan Atribut',
            'RuntimeError': 'Kesalahan Runtime',
            'Exception': 'Kesalahan Umum',
            'UnexpectedToken' : 'Token atau Kata Kunci Tidak Diketahui',
            'UnexpectedCharacters' : 'Karakter tidak diketahui'
        }

        error_type = type(e).__name__
        translated_error = error_translations.get(error_type, error_type)

        css = """ 
                <style>
        .tarri-error-container {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            margin: 15px 0;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        .error-header {
            background: #f8fafc;
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .error-title {
            font-weight: 600;
            color: #2d3748;
            font-size: 16px;
            display: flex;
            align-items: center;
        }
        .error-icon {
            margin-right: 8px;
            font-size: 18px;
        }
        .error-type-badge {
            background: #edf2f7;
            color: #4a5568;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        .error-content {
            padding: 16px;
            background: white;
        }
        .error-message {
            color: #e53e3e;
            font-weight: 500;
            margin-bottom: 12px;
            font-size: 15px;
            padding: 10px;
            background: #fef2f2;
            border-radius: 4px;
            border-left: 3px solid #f56565;
        }
        .error-details {
            margin-top: 16px;
        }
        .error-details-title {
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 8px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .error-trace {
            background: #f7fafc;
            padding: 12px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #4a5568;
            white-space: pre-wrap;
            overflow-x: auto;
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
        }
        .error-help {
            margin-top: 16px;
            padding: 12px;
            background: #ebf8ff;
            border-radius: 4px;
            border-left: 3px solid #4299e1;
            font-size: 14px;
            color: #2b6cb0;
        }
        .error-help-title {
            font-weight: 600;
            margin-bottom: 6px;
        }
        
        .center {
            text-align: center;
        }
        .footer {
            margin-top: 20px;
            padding: 12px;
            color: #718096;
            font-size: 12px;
            border-top: 1px solid #e2e8f0;
        }
        </style>
        """

        help_suggestions = {
            'SyntaxError': 'Periksa kembali sintaks kode Kamu. Pastikan semua tKamu kurung, titik koma, dan tKamu baca lainnya digunakan dengan benar.',
            'NameError': 'Variabel atau fungsi yang Kamu coba gunakan belum didefinisikan. Periksa ejaan atau pastikan Kamu telah mendefinisikannya.',
            'TypeError': 'Kamu mungkin mencoba melakukan operasi pada tipe data yang tidak sesuai. Periksa tipe data variabel yang digunakan.',
            'IndexError': 'Indeks yang Kamu coba akses tidak ada dalam koleksi. Pastikan indeks berada dalam rentang yang valid.',
            'KeyError': 'Kunci yang Kamu coba akses tidak ada dalam dictionary. Periksa ejaan atau pastikan kunci tersebut telah ditambahkan.',
            'ZeroDivisionError': 'Tidak dapat melakukan pembagian dengan nol. Tambahkan pengecekan untuk memastikan pembagi tidak nol.',
            'ImportError': 'Modul atau library yang Kamu coba impor tidak dapat ditemukan. Pastikan nama modul benar dan telah terinstall.',
            'AttributeError': 'Objek tidak memiliki atribut atau metode yang Kamu coba akses. Periksa dokumentasi untuk atribut yang tersedia.',
            'UnexpectedToken' : 'Kata kunci atau perintah yang Kamu masukkan tidak diketahui. Atau mungkin lupa menggunakan titikawal{}?',
            'UnexpectedCharacters' : 'Kamu memasukkan karakter yang tidak diketahui. Mungkin ada salah tanda baca.',
            'default': 'Periksa dokumentasi untuk informasi lebih lanjut tentang kesalahan ini.'
        }
        help_message = help_suggestions.get(error_type, help_suggestions['default'])

        error_html = f"""
        <div class="tarri-error-container">
            <div class="error-header">
                <div class="error-title">
                    <span class="error-icon">⚠️</span>
                    {translated_error} | {get_tarri_version()}
                </div>
                <div class="error-type-badge">{error_type}</div>
            </div>
            <div class="error-content">
                <div class="error-help">
                    <div class="error-help-title">💡 Saran Pemecahan</div>
                    {help_message}
                </div>
            </div>
            <div class="footer center">
                TARRI Runtime Error • {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        </div>
        """

        return f"{css}{error_html}", {}


def build_context(environ):
    """Bangun request context (_GET, _POST, _REQUEST) dari WSGI environ"""
    method = environ.get("REQUEST_METHOD", "GET")
    if method == "GET":
        qs = environ.get("QUERY_STRING", "")
        data = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(qs).items()}
    elif method == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            size = 0
        body = environ["wsgi.input"].read(size).decode()
        data = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()}
    else:
        data = {}

    return {
        "_GET": data if method == "GET" else {},
        "_POST": data if method == "POST" else {},
        "_REQUEST": data
    }

