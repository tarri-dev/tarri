#==============================================================================#
# File    : cli.py                                                             #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Antarmuka Baris Perintah (CLI) utama Tarri: menangani argumen terminal     #
#   dan menjalankan file .tarri.                                               #
#==============================================================================#

import sys
import os
import time
from lark import Lark, UnexpectedInput
from tarri.repl.repl import tarri_repl


from .help import show_help
from .informasi import show_informasi

from tarri.interpreter.core import Context

from tarri.parser_global import parser
from tarri import __version__
from lark import Tree, Token
from tarri.loging import logger
from tarri.errors import TarriRuntimeError

try:
    from tarriweb.server import ROOT_DIR
except ModuleNotFoundError:
    ROOT_DIR = None


GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Load grammar
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    tarri_grammar = f.read()

parser = Lark(tarri_grammar, start="start", parser="lalr")


def run_file(
    filename: str, status: bool = False, show_ast: bool = False, cli_args=None
):
    """Jalankan file .tarri dengan dukungan argumen CLI (_argumen)."""
    start_time = time.perf_counter()
    interpreter = Context(root_project=ROOT_DIR if ROOT_DIR else ".")

    if cli_args is None:
        cli_args = []

    # Inject variabel global _argumen (mirip sys.argv di Python)
    # interpreter.global_scope["_argumen"] = cli_args
    interpreter.context["_argumen"] = cli_args

    try:
        if status:
            print()
            print(f"[tarri | cli] program dimulai ... (sukses)")

        if not filename.endswith(".tarri"):
            print()
            print(f"[tarri | cli] kesalahan! ekstensi file {filename} tidak dikenali ")
            print()
            return

        if not os.path.exists(filename):
            if status:
                print(
                    f"[tarri | cli] membaca file {os.path.basename(filename)} (gagal)"
                )
            print(f"[tarri | cli] kesalahan! file {filename} tidak ditemukan")
            print()
            return

        if status:
            print(f"[tarri | cli] membaca file {os.path.basename(filename)} (sukses)")

        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        if status:
            print(f"[tarri | cli] parsing kode sumber ...")

        tree = parser.parse(source)

        if status:
            print(f"[tarri | cli] parsing selesai (sukses)")

        # === Pretty printer AST ===
        def pretty_ast(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            lines = []
            if isinstance(node, Tree):
                label = node.data
                lines.append(prefix + connector + label)
                child_prefix = prefix + ("    " if is_last else "│   ")
                for i, child in enumerate(node.children):
                    last = i == len(node.children) - 1
                    lines.append(pretty_ast(child, child_prefix, last))
            elif isinstance(node, Token):
                lines.append(prefix + connector + f"{node.type}: {node.value}")
            return "\n".join(lines)

        if show_ast:
            print("\nAST DIMULAI")
            print(pretty_ast(tree, "", True))
            print("AST SELESAI\n")

        # Jalankan program
        interpreter.run(tree)

        end_time = time.perf_counter()
        duration = end_time - start_time
        print()
        print(f"[tarri | cli] program selesai dijalankan {duration:.4f} detik")

    except FileNotFoundError:
        if status:
            print()
            print(f"[tarri | cli] membaca file {os.path.basename(filename)} (gagal)")
        print(f"[tarri | cli] kesalahan! file {filename} tidak ditemukan")
        print()

    except UnexpectedInput as e:
        print(f"[tarri | cli] proses penguraian program ... (gagal)")
        baris = getattr(e, "line", "?")
        kolom = getattr(e, "column", "?")
        print(f"[tarri | cli] posisi kesalahan : baris {baris}, kolom {kolom}")
        try:
            context_line = e.get_context(source, 1)
            print(context_line)
        except Exception:
            print("    ^")
        print()

    except TarriRuntimeError as e:
        raise e  # Re-raise TarriRuntimeError to be handled by the interpreter's try-catch
    except Exception as e:
        print()
        pesan = str(e)
        terjemahan = {
            "list index out of range": "indeks daftar melebihi batas",
            "division by zero": "pembagian dengan nol tidak diizinkan",
            "name": "variabel tidak dikenal",
            "syntax": "kesalahan penulisan kode (sintaks)",
            "type": "kesalahan tipe data",
            "value": "nilai tidak valid",
            "file": "berkas tidak ditemukan",
            "key": "kunci tidak ditemukan di kamus",
            "attribute": "atribut tidak ditemukan pada objek",
            "index": "indeks di luar batas",
            "zero": "pembagian dengan nol",
            "recursion": "rekursi terlalu dalam — kemungkinan rekursi tak terbatas",
            "unicode": "kesalahan karakter — teks tidak bisa dibaca",
            "memory": "kehabisan memori",
        }
        pesan_id = next(
            (terjemahan[k] for k in terjemahan if k in pesan.lower()), pesan
        )
        print(f"[tarri | cli] kesalahan : {pesan_id}")
        print()


def main():
    args = sys.argv[1:]  # ambil argumen tanpa nama script

    try:
        # ================================================#
        # MODE INTERAKTIF (REPL)
        # ================================================#
        if not args or args[0] in ("repl", "live", "interaktif"):
            # Pastikan logger tidak mengganggu stdout
            # Hanya aktifkan file logging, REPL tetap normal
            tarri_repl()
            return

        # ================================================#
        # BANTUAN & INFORMASI
        # ================================================#
        if args[0] in ("-b", "--bantuan"):
            show_help()
            return

        if args[0] in ("-i", "--informasi"):
            show_informasi()
            return

        # ================================================#
        # CEK VERSI
        # ================================================#
        if args[0] in ("--versi", "-v", "versi"):
            print(f"Tarri | {__version__}")
            return

        # ================================================#
        # SUBCOMMAND: jalankan
        # ================================================#
        if args[0] in ("jalankan", "j", "mulai", "."):
            if len(args) < 2:
                print()
                print(f"[tarri | cli] kesalahan! : nama file .tarri tidak diberikan")
                print()
                return

            filename = args[1]
            status = "--status" in args
            show_ast = "--ast" in args
            extra_args = [a for a in args[2:] if not a.startswith("--")]

            run_file(filename, status=status, show_ast=show_ast, cli_args=extra_args)
            return

        # ===============================
        # Lihat log
        # ===============================
        if args and args[0] == "log":
            # Gunakan try/finally agar stdout selalu kembali ke normal
            original_stdout = sys.stdout
            try:
                sys.stdout = sys.__stdout__

                # Subcommand hapus
                if len(args) > 1 and args[1] == "hapus":
                    print()
                    konfirmasi = (
                        input("[tarri | cli] Hapus semua log? (ya/tidak): ")
                        .strip()
                        .lower()
                    )
                    if konfirmasi == "ya":
                        log_dir = os.path.expanduser("~/.tarri/logs")
                        if os.path.exists(log_dir):
                            files = os.listdir(log_dir)
                            for f in files:
                                try:
                                    os.remove(os.path.join(log_dir, f))
                                except Exception as e:
                                    print(f"[tarri | cli] Gagal menghapus {f}: {e}")
                            print("[tarri | cli] Semua log berhasil dihapus.")
                        else:
                            print("[tarri | cli] Tidak ada folder log ditemukan.")
                    else:
                        print("[tarri | cli] Batal menghapus log.")
                    print()
                    return

                # Subcommand lihat log biasa
                print()
                print("[tarri | cli] Menampilkan log terakhir (50 baris)")
                print(f"Lokasi: {logger.log_file}")

                try:
                    with open(logger.log_file, "r", encoding="utf-8") as f:
                        all_lines = f.readlines()
                        tail = all_lines[-50:] if len(all_lines) > 50 else all_lines
                        for line in tail:
                            parts = line.split("] ", 1)
                            if len(parts) > 1:
                                print(parts[1].strip())
                            else:
                                print(line.strip())
                except FileNotFoundError:
                    print("[tarri | cli] Tidak ada log ditemukan.")

                print("[tarri | cli] Selesai menampilkan log\n")
            finally:
                sys.stdout = original_stdout  # kembalikan stdout apa pun yang terjadi
            return

        # ================================================#
        # PERINTAH TIDAK DIKENAL
        # ================================================#
        print(
            f"[tarri | cli] perintah tidak diketahui, periksa bantuan ( -b / --bantuan )"
        )

    except KeyboardInterrupt:
        print()
        print(f"[tarri | cli] Program telah dihentikan oleh pengguna.")
        return 0


if __name__ == "__main__":
    main()
