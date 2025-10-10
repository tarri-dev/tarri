# ==============================================================================#
# repl.py - Mode Interaktif Bahasa TARRI dengan Auto-Completion (Cross-Platform)#
# Teknologi Algoritmik Representasi Rekayasa Indonesia                          #
# ------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                          #
# Lisensi : MIT                                                                 #
# ------------------------------------------------------------------------------#

from lark import Lark, UnexpectedInput
from tarri.interpreter.core import Context
from datetime import datetime
import readline
import platform
import os
import subprocess
import sys
import time

# Lokasi grammar.lark
GRAMMAR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "grammar.lark")

# Parser global
parser = Lark.open(GRAMMAR_PATH, start="start", parser="lalr")

# Kata kunci utama bahasa Tarri
TARRI_KEYWORDS = [
    "titikawal", "fungsi", "kembalikan", "jika", "ataujika", "lainnya",
    "selama", "ulangi", "untuk", "setiap", "setiapdari", "benar", "salah",
    "kosong", "bukan", "tampilkan", "sembunyikan", "hentikan", "lanjutkan",
    "kelas", "cetak", "hampa", "coba"
]

# Perintah REPL
REPL_COMMANDS = ["keluar", "bersihkan", "clear", "cls"]

ALL_COMPLETIONS = TARRI_KEYWORDS + REPL_COMMANDS

# Warna terminal (ANSI escape codes)
RED = "\033[91m"
RESET = "\033[0m"


def tarri_completer(text, state):
    """Sistem auto-complete sederhana"""
    options = [w for w in ALL_COMPLETIONS if w.startswith(text)]
    return options[state] if state < len(options) else None


def setup_readline():
    """Aktifkan auto-completion di semua OS"""
    completer = tarri_completer
    readline.set_completer(completer)

    # Deteksi apakah pakai libedit (macOS)
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")  # Tab = complete (libedit)
    else:
        readline.parse_and_bind("tab: complete")        # GNU readline

    # History file
    history_path = os.path.expanduser("~/.tarri_history")
    if os.path.exists(history_path):
        readline.read_history_file(history_path)
    return history_path


def clear_screen():
    """Bersihkan terminal"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        


def get_tarri_version():
    """Ambil versi Tarri dari command line"""
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
    
def get_datetime():
    """Ambil tanggal dan waktu sekarang"""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def loading(msg="Memulai Mode Interaktif Tarri"):
    for c in msg + "...":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    print()


def tarri_repl():
    waktu_mulai = get_datetime()
    loading()
    print(f"[TARRI | Mode Interaktif] {get_tarri_version()} | {waktu_mulai}")
    print(f"Ketik {RED}'keluar'{RESET} untuk berhenti atau {RED}'bersihkan'{RESET} untuk membersihkan layar.")
    print(f"bahasatarri.com | github.com/tarri-dev | instagram.com/bahasatarri")
    print()

    ctx = Context(root_project=".")
    ctx.is_repl = True
    buffer = ""

    history_path = setup_readline()

    try:
        while True:
            try:
                prompt = f"{RED}  ... {RESET}" if buffer else f"{RED}[>>>]{RESET} "
                line = input(prompt)

                # --- keluar ---
                if line.strip().lower() in ["keluar", "exit", "quit"]:
                    print("Sampai jumpa 👋")
                    break

                # --- bersihkan layar ---
                if line.strip().lower() in ["bersihkan", "clear", "cls"]:
                    clear_screen()
                    continue

                buffer += line + "\n"

                # lanjut jika blok belum lengkap
                if buffer.count("{") > buffer.count("}"):
                    continue

                kode = buffer.strip()
                buffer = ""

                if not kode:
                    continue

                # Auto-wrap titikawal
                # Deteksi input yang perlu atau tidak perlu dibungkus titikawal
                PERLU_TITIKAWAL = True
                AWALAN_BLOK = (
                    "titikawal", "fungsi", "kelas", "jika", "ataujika", "lainnya",
                    "selama", "ulangi", "ulangidari", "setiap", "setiapdari",
                    "untuk"
                )

                for awal in AWALAN_BLOK:
                    if kode.strip().startswith(awal):
                        PERLU_TITIKAWAL = False
                        break

                # Jika ekspresi sederhana (misal: cetak(...), 5+6, _buah[2 hingga 4])
                if PERLU_TITIKAWAL:
                    kode = f"titikawal {{ {kode} }}"


                tree = parser.parse(kode)
                hasil = ctx.run(tree)

                if hasil is not None:
                    print(hasil)

            except UnexpectedInput as e:
                # 🔹 Tangkap informasi kesalahan dari Lark
                baris = getattr(e, 'line', '?')
                kolom = getattr(e, 'column', '?')
                token = None
                prev_token = None

                if hasattr(e, 'token') and e.token:
                    token = e.token
                if hasattr(e, 'prev_token') and e.prev_token:
                    prev_token = e.prev_token

                simbol = token.value if token else "?"
                sebelumnya = prev_token.value if prev_token else "?"

                print(f"{RED}[tarri]{RESET} Kesalahan sintaks di baris {baris}. Periksa penulisan tanda variabel, kurung, operator, atau struktur blok kode.")
                print("")

                buffer = ""

            except KeyboardInterrupt:
                print("\n(^C ditekan) — ketik 'keluar' untuk berhenti.")
                buffer = ""
            except Exception as e:
                print(f"[tarri | repl] kesalahan eksekusi: {e}")
                buffer = ""

    finally:
        try:
            readline.write_history_file(history_path)
        except Exception:
            pass
