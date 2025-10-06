# tarri/help.py

import subprocess

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

def show_informasi():
    print(f"""
{BLUE}
INFORMASI BAHASA TARRI
{RESET}
Bahasa Tarri adalah bahasa pemrograman dengan sintaks penuh Bahasa Indonesia.
Didesain agar siapa pun – baik pelajar, mahasiswa, peneliti, maupun praktisi –
bisa menulis program komputer dengan bahasa sehari-hari tanpa harus menghafal
keyword asing seperti 'if', 'while', atau 'print'.

{BLUE}Tujuan utama Tarri:{RESET}
  - Memberikan jembatan bagi pemula untuk memahami konsep pemrograman
    tanpa terhalang oleh bahasa asing.
  - Menjadi bukti bahwa Bahasa Indonesia mampu berdiri sejajar dengan
    bahasa-bahasa pemrograman lain di dunia.
  - Mendukung eksperimen akademis, riset, dan inovasi teknologi
    berbasis lokal yang lebih mudah diakses.
  - Menyediakan runtime yang ringan, cepat, dan sederhana
    sehingga cocok untuk edukasi maupun prototyping.

{BLUE}Filosofi desain Tarri:{RESET}

  - {BLUE}Mudah dipahami:{RESET} Sintaks dibuat mirip percakapan sehari-hari.
  - {BLUE}Transparan:{RESET} Setiap instruksi memiliki padanan jelas dalam
    Bahasa Indonesia tanpa terjemahan ambigu.
  - {BLUE}Ringan:{RESET} Interpreter ditulis dengan Python, mudah dijalankan
    di berbagai platform.
  - {BLUE}Terbuka:{RESET} Tarri adalah proyek open source yang bisa dikembangkan
    bersama komunitas.

Saat ini Tarri telah mencapai versi {get_tarri_version()}, dan sudah mendukung
banyak konstruksi dasar pemrograman seperti:

  - {BLUE}fungsi(){RESET}  → untuk mendefinisikan sebuah fungsi
  - {BLUE}cetak(){RESET}   → untuk menampilkan teks ke layar
  - {BLUE}titikawal{RESET} → entry point program
  - {BLUE}tampilkan{RESET} → untuk memanggil fungsi atau hasil keluaran


{BLUE}situs resmi   : bahasatarri.com{RESET}
{BLUE}github        : github.com/tarri-dev{RESET}
{BLUE}instagram     : instagram.com/bahasatarri{RESET}

{RED}Teknologi Algoritmik Representasi Rekayasa Indonesia{RESET}
""")
