from pathlib import Path
from lark import Tree
import io, contextlib
from tarri.parser_global import parser

def termasuk(interpreter, args):
    if not args:
        return

    filename = str(args[0]).strip().strip('"').strip("'")

    # Base dir dari file utama
    if hasattr(interpreter, "root_file") and interpreter.root_file:
        base_dir = Path(interpreter.root_file).parent
    else:
        base_dir = Path.cwd()

    file_path = (base_dir / filename).resolve()

    if not file_path.exists():
        print(f"[tarri] kesalahan : file '{filename}' tidak ditemukan")
        return

    source = file_path.read_text(encoding="utf-8")

    try:
        tree = parser.parse(source)
        old_file = getattr(interpreter, "current_file", None)
        interpreter.current_file = str(file_path)

        # Pakai buffer sementara
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            interpreter.run(tree)

        # Cetak semua output buffer ke browser
        output = buf.getvalue()
        if output:
            print(output, end="")  # HTML dari cetak_henti atau print lain tetap muncul

        interpreter.current_file = old_file

    except Exception as e:
        # Tampilkan buffer sebelum error
        if 'buf' in locals():
            print(buf.getvalue(), end="")
        print(f"[tarri] kesalahan : {e}")
