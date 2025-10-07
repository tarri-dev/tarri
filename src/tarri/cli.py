import sys
import os
import time
from lark import Lark, UnexpectedInput

from .help import show_help
from .informasi import show_informasi

from tarri.interpreter.core import Context

from tarri.parser_global import parser
from tarri import __version__
from lark import Tree, Token


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


def run_file(filename: str, status: bool = False, show_ast: bool = False):
    """Jalankan file .tarri"""
    start_time = time.perf_counter()
    interpreter = Context(root_project=ROOT_DIR if ROOT_DIR else ".")


    try:
        if status:
            print()
            print(f"[tarri | cli] program dimulai ... {GREEN}(sukses){RESET}")

        if not filename.endswith(".tarri"):
            print()
            print(f"[tarri | cli] {RED}kesalahan!{RESET} ekstensi file {BLUE}{filename}{RESET} tidak dikenali {RESET}")
            print()
            return

        if not os.path.exists(filename):
            if status:
                print(f"[tarri | cli] membaca file {BLUE}{os.path.basename(filename)}{RESET} {RED}(gagal){RESET}")
            print(f"[tarri | cli] {RED}kesalahan!{RESET} file {BLUE}{filename}{RESET} tidak ditemukan")
            print()
            return

        if status:
            print(f"[tarri | cli] membaca file {BLUE}{os.path.basename(filename)}{RESET} {GREEN}(sukses){RESET}")

        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        if status:
            print(f"[tarri | cli] parsing kode sumber ...")

        tree = parser.parse(source)

        if status:
            print(f"[tarri | cli] parsing selesai {GREEN}(sukses){RESET}")
        
        def pretty_ast(node, prefix="", is_last=True):
            """AST printer rapi dengan garis cabang"""
            connector = "└── " if is_last else "├── "
            lines = []

            # Label node
            if isinstance(node, Tree):
                label = node.data
                if label == "loop_stmt":
                    # Tambahkan ringkasan kalau loop
                    try:
                        var = node.children[0].value
                        start = node.children[2].children[0].value
                        end = node.children[3].children[0].value
                        label = f"loop_stmt (for {var} = {start} → {end})"
                    except Exception:
                        pass
                lines.append(prefix + connector + label)

                # anak-anak
                child_prefix = prefix + ("    " if is_last else "│   ")
                for i, child in enumerate(node.children):
                    last = (i == len(node.children) - 1)
                    lines.append(pretty_ast(child, child_prefix, last))

            elif isinstance(node, Token):
                lines.append(prefix + connector + f"{node.type}: {node.value}")

            return "\n".join(lines)

        # Pemakaian
        if show_ast:
            print("\nAST DIMULAI")
            print(pretty_ast(tree, "", True))
            print("AST SELESAI\n")

                
        interpreter.run(tree)
        

        end_time = time.perf_counter()
        duration = end_time - start_time
        print()
        print(f"[tarri | cli] program selesai dijalankan {BLUE}{duration:.4f}{RESET} detik")

    except FileNotFoundError:
        if status:
            print()
            print(f"[tarri | cli] membaca file {BLUE}{os.path.basename(filename)}{RESET} {RED}(gagal){RESET}")
        print(f"[tarri | cli] {RED}kesalahan!{RESET} file {BLUE}{filename}{RESET} tidak ditemukan")
        print()

    
    except UnexpectedInput as e:
        print(f"[tarri | cli] proses parsing ... {RED}(gagal){RESET}")
        line = getattr(e, "line", "?")
        column = getattr(e, "column", "?")
        print(f"[tarri | cli] posisi {RED}kesalahan!{RESET} : line {line}, column {column}")
        try:
            context_line = e.get_context(source, 1) 
            print(context_line)
        except Exception:
            print("    ^")

        print()

    except Exception as e:
        print()
        print(f"[tarri | cli] {RED}kesalahan{RESET} : {e}{RESET}")
        print()


def main():
    args = sys.argv[1:]  # ambil argumen tanpa nama script

    try:
        
        # Tidak ada argumen atau -b / --bantuan
        if not args or args[0] in ("-b", "--bantuan"):
            show_help()
            return
        
        if not args or args[0] in ("-i", "--informasi"):
            show_informasi()
            return
        
        # Cek versi
        if args[0] in ("--versi", "-v", "versi"):
            from tarri import __version__
            print(f"Tarri | {__version__}")
            return

        # Subcommand jalankan
        if args[0] in ("jalankan", "j", "mulai", "."):
            if len(args) < 2:
                print()
                print(f"[tarri | cli] {RED}kesalahan!{RESET}: nama file .tarri tidak diberikan")
                print()
                return

            # mode normal → jalankan file .tarri
            filename = args[1]
            status = "--status" in args
            show_ast = "--ast" in args
            run_file(filename, status=status, show_ast=show_ast)
            return

        # Semua perintah lain → tidak dikenal
        print(f"[tarri | cli] perintah tidak diketahui, periksa bantuan ( -b / --bantuan )")

    except KeyboardInterrupt:
        print()
        print(f"[tarri | cli] {RED}Program telah dihentikan oleh pengguna.{RESET}")
        return 0


if __name__ == "__main__":
    main()
