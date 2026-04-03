#==============================================================================#
# File    : cetak_web.py                                                       #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'cetak_web' yang tersedia dalam bahasa          #
#   Tarri.                                                                     #
#==============================================================================#

# from tarri.parser_global import parser
import html
import json
import sys


def cetak_web(interpreter, args):
    if not args:
        return

    bagian = []  # kumpulan baris output

    for value in args:

        # Jika value adalah nama variabel Tarri (diawali "_")
        if isinstance(value, str) and value.startswith("_"):
            val = interpreter.context.get(
                value, f"[tarri | cetak_web] variabel '{value}' tidak ditemukan"
            )
        else:
            val = value

        # Jika dict/list format rapi dengan indent
        if isinstance(val, (dict, list)):
            formatted = json.dumps(val, ensure_ascii=False, indent=4)
        else:
            formatted = str(val)

        bagian.append(formatted)

    # 🔥 Gabungkan dengan newline 🔥
    final_text = "\n".join(bagian)

    # Escape HTML agar aman
    safe_output = html.escape(final_text)

    output_html = f"""
<pre>
{safe_output}
</pre>
"""

    # Mode CLI vs Browser
    if sys.stdout.isatty():
        print(f"[tarri | cetak_web]\n{final_text}")
    else:
        print(output_html)

    raise StopIteration(output_html)
