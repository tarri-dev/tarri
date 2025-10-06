# tarri/help.py

import subprocess


# Definisikan warna di sini supaya tidak perlu file cli_colors terpisah
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

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
      
def show_help():
    print(f"""
    
{BLUE}{get_tarri_version()}{RESET}

{BLUE}Contoh penggunaan:{RESET}

      tarri jalankan contoh.tarri

{BLUE}Perintah utama:{RESET}

      jalankan  <namaprogram.tarri>       Jalankan file .tarri
      --status                            Tampilkan log status eksekusi
      --ast                               Tampilkan AST hasil parsing
      -b / --bantuan                      Menampilkan menu bantuan
      -i / --informasi                    Menampilkan menu informasi
      -v / --versi / versi                Menampilkan versi bahasa tarri
      
{BLUE}situs      : bahasatarri.com{RESET}
{BLUE}github     : github.com/tarri-dev{RESET}
{BLUE}instagram  : instagram.com/bahasatarri{RESET}

{RED}Teknologi Algoritmik Representasi Rekayasa Indonesia{RESET}
""")
