#==============================================================================#
# File    : termasuk.py                                                        #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'termasuk' yang tersedia dalam bahasa           #
#   Tarri.                                                                     #
#==============================================================================#

from pathlib import Path
from lark import Tree
import io, contextlib
from tarri.parser_global import parser


def termasuk(interpreter, args):
    """
    Memasukkan file .tarri lain ke interpreter.
    Mengembalikan 'Benar' jika file berhasil dimuat dan dijalankan,
    'Salah' jika file tidak ditemukan atau gagal.
    """
    if not args:
        print("[tarri] kesalahan : nama file tidak diberikan")
        return "Salah"

    filename = str(args[0]).strip().strip('"').strip("'")

    # Daftar folder yang akan dicoba
    possible_dirs = []
    if hasattr(interpreter, "root_file") and interpreter.root_file:
        possible_dirs.append(Path(interpreter.root_file).parent)
    possible_dirs.append(Path.cwd())

    file_path = None
    for d in possible_dirs:
        candidate = (d / filename).resolve()
        if candidate.exists():
            file_path = candidate
            break

    if not file_path:
        print(
            f"[tarri] kesalahan : file '{filename}' tidak ditemukan di folder: {[str(d) for d in possible_dirs]}"
        )
        return "Salah"

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = parser.parse(source)
    except Exception as e:
        print(f"[tarri] kesalahan membaca/parse file '{file_path}': {e}")
        return "Salah"

    old_file = getattr(interpreter, "current_file", None)
    interpreter.current_file = str(file_path)

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            interpreter.run(tree)
    except Exception as e:
        # Tampilkan buffer sebelum error
        print(buf.getvalue(), end="")
        print(f"[tarri] kesalahan saat mengeksekusi file '{file_path}': {e}")
        interpreter.current_file = old_file
        return "Salah"
    else:
        # Cetak semua output buffer ke browser
        output = buf.getvalue()
        if output:
            print(output, end="")
        return "Benar"
    finally:
        interpreter.current_file = old_file
