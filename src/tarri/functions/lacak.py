import os
import sys
import time
import getpass
import platform
import datetime

def lacak(interpreter, args=None):
    """Pelacakan penuh Tarri — menampilkan info sistem, interpreter, dan variabel aktif."""

    mulai = time.time()
    waktu_mulai = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")

    print("\n" + "="*75)
    print(f"LACAK PROGRAM — {waktu_mulai}")
    print("="*75)

    # 1. INFORMASI SISTEM
    print("\nSISTEM OPERASI")
    print("-"*75)
    try:
        print(f"{'Nama OS':20} : {platform.system()} {platform.release()} ({platform.machine()})")
        print(f"{'Versi Python':20} : {platform.python_version()}")
        print(f"{'Nama Pengguna':20} : {getpass.getuser()}")
        print(f"{'Folder Aktif':20} : {os.getcwd()}")
        print(f"{'Waktu Saat Ini':20} : {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    except Exception as e:
        print(f"(Gagal membaca info sistem: {e})")

    # 2. INFORMASI INTERPRETER TARRI
    print("\nINTERPRETER TARRI")
    print("-"*75)
    try:
        try:
            import tarri
            versi = getattr(tarri, "__version__", "tidak diketahui")
        except Exception:
            versi = "tidak diketahui"

        file_sumber = getattr(interpreter, "source_path", None)
        mode = getattr(interpreter, "mode", None)

        # fallback otomatis
        if not file_sumber:
            if len(sys.argv) > 1 and sys.argv[1].endswith(".tarri"):
                file_sumber = sys.argv[1]
            else:
                file_sumber = os.path.basename(sys.argv[0]) or "(interaktif)"
        if not mode:
            mode = "CLI" if sys.stdin.isatty() else "Embedded"

        print(f"{'Versi Tarri':20} : {versi}")
        print(f"{'File Sumber':20} : {file_sumber}")
        print(f"{'Mode Eksekusi':20} : {mode}")
    except Exception as e:
        print(f"(Gagal membaca info interpreter: {e})")

    # 3. VARIABEL AKTIF
    print("\nVARIABEL AKTIF")
    print("-"*75)
    ctx = getattr(interpreter, "context", {})
    if not ctx:
        print("Tidak ada variabel aktif saat ini.")
    else:
        for nama, nilai in ctx.items():
            try:
                tipe = type(nilai).__name__
                tampil = str(nilai)
                if len(tampil) > 120:
                    tampil = tampil[:120] + "..."
                print(f"{'Nama':20} : {nama}")
                print(f"{'Isi':20} : {tampil}")
                print(f"{'Tipe':20} : {tipe}\n")
            except Exception as e:
                print(f"{'Nama':20} : {nama}")
                print(f"(Gagal membaca nilai: {e})\n")

    # 4. SESI AKTIF (opsional)
    sesi_obj = ctx.get("sesi") if isinstance(ctx, dict) else None
    if sesi_obj:
        print("\nSESI AKTIF")
        print("-"*75)
        try:
            if isinstance(sesi_obj, dict):
                for k, v in sesi_obj.items():
                    print(f"{k:20} : {v}")
            elif hasattr(sesi_obj, "to_dict"):
                for k, v in sesi_obj.to_dict().items():
                    print(f"{k:20} : {v}")
            else:
                print(f"(Sesi tidak dapat dibaca: {type(sesi_obj).__name__})")
        except Exception as e:
            print(f"(Gagal membaca sesi: {e})")

    # 5. ARGUMEN & WAKTU
    print("\nARGUMEN & WAKTU EKSEKUSI")
    print("-"*75)
    try:
        args_str = " ".join(sys.argv)
        print(f"{'Argumen CLI':20} : {args_str}")
    except Exception:
        print(f"{'Argumen CLI':20} : (tidak dapat dibaca)")

    durasi = time.time() - mulai
    print(f"{'Durasi Pelacakan':20} : {durasi:.4f} detik")

    print("="*75)
    print("Pelacakan selesai.\n")

    raise SystemExit("[tarri | lacak] Proses pelacakan dihentikan")
