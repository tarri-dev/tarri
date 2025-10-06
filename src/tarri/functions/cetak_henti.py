# tarri/src/tarri/functions/cetak_henti.py
from tarri.parser_global import parser
import io, contextlib, html
import subprocess
import json

# import time
# t0 = time.time()
# # proses render
# t1 = time.time()
# print(f"[tarri | cetak_henti] waktu render cetak_henti: {t1 - t0:.4f} detik")


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

def cetak_henti(interpreter, args):
    """
    Fungsi TARRI cetak_henti() atau ch()
    - Menampilkan isi variabel ke halaman HTML
    - Hentikan eksekusi setelah menampilkan
    """
    if not args:
        return

    # Ambil nilai pertama
    value = args[0]

    # Jika value adalah nama variabel, coba ambil dari context interpreter
    if isinstance(value, str) and value.startswith("_"):
        val = interpreter.context.get(value, f"[tarri | cetak_henti] variabel '{value}' tidak ditemukan")
    else:
        val = value

    # Format output dengan JSON untuk dict/list
    if isinstance(val, (dict, list)):
        formatted_value = json.dumps(val, indent=4, ensure_ascii=False)
    else:
        formatted_value = str(val)

    # Escape HTML untuk keamanan
    safe_output = html.escape(formatted_value)
    
    # Dapatkan tipe data dari nilai
    value_type = type(val).__name__

    # CSS untuk styling error (gaya Laravel-like)
    css = """
    <style>
    .tarri-dump-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
        margin: 15px 0;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .dump-header {
        background: #f8fafc;
        padding: 12px 16px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .dump-title {
        font-weight: 600;
        color: #2d3748;
        font-size: 16px;
        display: flex;
        align-items: center;
    }
    .dump-icon {
        margin-right: 8px;
        font-size: 18px;
    }
    .dump-type-badge {
        background: #edf2f7;
        color: #4a5568;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
    }
    .dump-content {
        padding: 16px;
        background: white;
    }
    .dump-value {
        background: #f7fafc;
        padding: 12px;
        border-radius: 4px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 13px;
        line-height: 1.5;
        color: #2d3748;
        white-space: pre-wrap;
        overflow-x: auto;
        border: 1px solid #e2e8f0;
    }
    .dump-info {
        margin-top: 12px;
        padding: 8px 12px;
        background: #ebf8ff;
        border-radius: 4px;
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
    
    # Format HTML untuk output
    output_html = f"""
    {css}
    <div class="tarri-dump-container">
        <div class="dump-header">
            <div class="dump-title">
                Output cetak_henti() | {get_tarri_version()}
            </div>
            <div class="dump-type-badge">{value_type}</div>
        </div>
        <div class="dump-content">
            <div class="dump-value">{safe_output}</div>
            
            <div class="dump-info">
                <strong>💡 Informasi:</strong> Eksekusi dihentikan oleh fungsi cetak_henti()
            </div>
            
            <div class="footer center">
                TARRI Debug Output • Dihentikan secara manual
            </div>
        </div>
    </div>
    """

    # Cetak ke stdout (yang nanti ditangkap replace_tarri_with_output)
    print(output_html)
    raise StopIteration(output_html)
    # Hentikan eksekusi dengan exception custom
    # raise StopIteration("[tarri | cetak_henti] eksekusi dihentikan oleh cetak_henti()")

# Alias pendek
ch = cetak_henti