import sys
import os
import time
from lark import Lark, UnexpectedInput

from .help import show_help
from .interpreter import Interpreter

# Warna ANSI (opsional, bisa pakai dari help.py)
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Load grammar
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    tarri_grammar = f.read()

parser = Lark(tarri_grammar, start="start", parser="lalr")


def run_file(filename: str, status: bool = False, show_ast: bool = False):
    """Jalankan file .tarri"""
    start_time = time.perf_counter()
    interpreter = Interpreter()

    try:
        if status:
            print()
            print(f"[tarri] program dimulai ... {GREEN}(sukses){RESET}")

        if not filename.endswith(".tarri"):
            print()
            print(f"[tarri] {RED}kesalahan!{RESET} ekstensi file {BLUE}{filename}{RESET} tidak dikenali {RESET}")
            print()
            return

        if not os.path.exists(filename):
            if status:
                print(f"[tarri] membaca file {BLUE}{os.path.basename(filename)}{RESET} {RED}(gagal){RESET}")
            print(f"[tarri] {RED}kesalahan!{RESET} file {BLUE}{filename}{RESET} tidak ditemukan")
            print()
            return

        if status:
            print(f"[tarri] membaca file {BLUE}{os.path.basename(filename)}{RESET} {GREEN}(sukses){RESET}")

        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        if status:
            print(f"[tarri] parsing kode sumber ...")

        tree = parser.parse(source)

        if status:
            print(f"[tarri] parsing selesai {GREEN}(sukses){RESET}")

        if show_ast:
            print(f"\n{BLUE}=== AST ==={RESET}")
            print(tree.pretty())
            print(f"{BLUE}===========\n{RESET}")

        interpreter.run(tree)

        end_time = time.perf_counter()
        duration = end_time - start_time
        print()
        print(f"[tarri] program selesai dijalankan {BLUE}{duration:.4f}{RESET} detik")

    except FileNotFoundError:
        if status:
            print()
            print(f"[tarri] membaca file {BLUE}{os.path.basename(filename)}{RESET} {RED}(gagal){RESET}")
        print(f"[tarri] {RED}kesalahan!{RESET} file {BLUE}{filename}{RESET} tidak ditemukan")
        print()
    except UnexpectedInput as e:
        print(f"[tarri] proses parsing ... {RED}(gagal){RESET}")
        print(f"[tarri] posisi {RED}kesalahan!{RESET} : line {e.line}, column {e.column}")
        print(e)
        print()
    except Exception as e:
        print()
        print(f"[tarri] {RED}kesalahan{RESET} : {e}{RESET}")
        print()


def main():
    args = sys.argv[1:]  # ambil argumen tanpa nama script

    try:
        # Tidak ada argumen atau -b / --bantuan
        if not args or args[0] in ("-b", "--bantuan"):
            show_help()
            return

        # Subcommand jalankan
        if args[0] in ("jalankan", "j", "mulai", ">>"):   # <-- tambahkan '>>' sebagai alias
            if len(args) < 2:
                print()
                print(f"[tarri] {RED}kesalahan!{RESET}: nama file .tarri tidak diberikan")
                print()
                return

            filename = args[1]
            status = "--status" in args
            show_ast = "--ast" in args
            run_file(filename, status=status, show_ast=show_ast)
            return

        # Semua perintah lain → tidak dikenal
        print(f"[tarri] perintah tidak diketahui, periksa bantuan ( -b / --bantuan )")

    except KeyboardInterrupt:
        print()
        print(f"[tarri] {RED}Program telah dihentikan oleh pengguna.{RESET}")
        return 0  # atau sys.exit(0)


if __name__ == "__main__":
    main()
