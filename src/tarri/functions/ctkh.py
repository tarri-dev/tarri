from tarri.parser_global import parser
import html
import json
import sys

def ctkh(interpreter, args):
    """
    cetak_HTML() atau ch()
    - menerima banyak argumen
    - semua argumen digabung tanpa newline
    - dict/list diformat JSON single-line
    """
    if not args:
        return

    bagian = []

    # Proses semua argumen
    for value in args:

        # Variabel Tarri (nama diawali "_")
        if isinstance(value, str) and value.startswith("_"):
            val = interpreter.context.get(
                value,
                f"[tarri | cetak_HTML] variabel '{value}' tidak ditemukan"
            )
        else:
            val = value

        # Format dict/list jadi JSON 1 baris
        if isinstance(val, (dict, list)):
            formatted = json.dumps(val, ensure_ascii=False)
        else:
            formatted = str(val)

        bagian.append(formatted)

    # 🔥 GABUNG TANPA NEWLINE, TANPA SPASI 🔥
    final_text = "".join(bagian)

    safe_output = html.escape(final_text)
    value_type = type(val).__name__

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

    output_html = f"""
    {css}
    <div class="tarri-dump-container">
        <div class="dump-header">
            <div class="dump-title">
                Hasil Cetak Versi HTML
            </div>
            <div class="dump-type-badge">{value_type}</div>
        </div>
        <div class="dump-content">
            <div class="dump-value">{safe_output}</div>
            
            <div class="dump-info">
                <strong>💡 Informasi:</strong> Eksekusi dihentikan oleh fungsi cetak_HTML()
            </div>
            
            <div class="footer center">
                TarriWeb • Dihentikan secara manual
            </div>
        </div>
    </div>
    """

    # Mode CLI
    if sys.stdout.isatty():
        print(f"[tarri | cetak_HTML] {final_text}")
    else:
        print(output_html)

    raise StopIteration(output_html)
