import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# --- KONFIGURASI PAKET ---
APP_NAME = "tarri"
VERSION = "0.8.2"
ARCH = "amd64" # Secara default 64-bit

def check_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        print("⚠️ Menginstal PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_entry_point():
    """Membuat file run_tarri.py sementara sebagai titik masuk utama bagi PyInstaller."""
    content = """import sys
import os
from tarri.cli import main

if __name__ == '__main__':
    # Pastikan aplikasi tidak terhenti oleh CWD
    main()
"""
    with open("run_tarri.py", "w") as f:
        f.write(content)

def build_binary():
    print("🚀 Mengompilasi Tarri menjadi executable...")
    
    separator = ";" if platform.system() == "Windows" else ":"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",
        # Membawa file grammar bawaan ke dalam executable
        f"--add-data=src/tarri/grammar.lark{separator}tarri",
        "--clean",
        "run_tarri.py"
    ]
    
    # Jalankan perintah tanpa menyembunyikan terminal
    subprocess.check_call(cmd)
    
    # Bersihkan file sampah build
    if os.path.exists("run_tarri.py"):
        os.remove("run_tarri.py")
    if os.path.exists(f"{APP_NAME}.spec"):
        os.remove(f"{APP_NAME}.spec")

def build_deb_folder():
    """Merakit struktur folder .deb untuk persiapan build."""
    binary_path = os.path.join("dist", APP_NAME)
    if not os.path.exists(binary_path):
        print("❌ Binari tidak ditemukan! Build gagal.")
        return
        
    deb_dir = f"{APP_NAME}_{VERSION}_{ARCH}"
    bin_dir = os.path.join(deb_dir, "usr", "local", "bin")
    opt_dir = os.path.join(deb_dir, "opt", APP_NAME)
    deb_metadata_dir = os.path.join(deb_dir, "DEBIAN")
    
    # Buat direktori
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(deb_metadata_dir, exist_ok=True)
    
    # Salin executable ke usr/local/bin
    shutil.copy2(binary_path, os.path.join(bin_dir, APP_NAME))
    
    # Buat file Control DEBIAN
    control_content = f"""Package: {APP_NAME}
Version: {VERSION}
Section: devel
Priority: optional
Architecture: {ARCH} # (Ubah menjadi 'all' jika untuk banyak platform)
Depends: 
Maintainer: Tarri Dev <bahasa.tarri@gmail.com>
Description: Bahasa Pemrograman Tarri
 Teknologi Algoritmik Representasi Rekayasa Indonesia.
 Mempermudah pelajar dari Indonesia belajar logika komputer.
"""
    with open(os.path.join(deb_metadata_dir, "control"), "w") as f:
        f.write(control_content)
        
    print(f"✅ Struktur folder .deb telah dibuat di folder: {deb_dir}/")
    print(f"📦 Untuk menggenerate file .deb hasil akhir (DI LINUX), ketik:")
    print(f"    dpkg-deb --build {deb_dir}")

def run():
    check_pyinstaller()
    create_entry_point()
    build_binary()
    
    # Struktur Deb dibuat terutama bila OS bukan windows
    if platform.system() != "Windows":
        build_deb_folder()
    else:
        print(f"✅ Build selesai! File eksekusi 'tarri.exe' tersedia di folder 'dist/'")

if __name__ == "__main__":
    run()
