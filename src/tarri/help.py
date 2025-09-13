# tarri/help.py

# Definisikan warna di sini supaya tidak perlu file cli_colors terpisah
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

def show_help():
    print(f"""
    
{RED}TARRI 0.0.1{RESET}

Perintah utama:

  tarri jalankan nama_program.tarri     Jalankan file .tarri
      --status                          Tampilkan log status eksekusi
      --ast                             Tampilkan AST hasil parsing
      -b / --bantuan                    Menampilkan menu bantuan

{RED}Contoh penggunaan:{RESET}
  tarri jalankan contoh.tarri --status --ast
""")
