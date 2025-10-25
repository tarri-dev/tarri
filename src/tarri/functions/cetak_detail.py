import os
import sys
import datetime
import platform
import getpass
import inspect
import types

# Peta tipe data Python → Bahasa Indonesia
TIPE_INDONESIA = {
    "str": "kata",
    "int": "angka bulat",
    "float": "angka desimal",
    "bool": "logika (benar/salah)",
    "list": "daftar",
    "tuple": "tupel",
    "dict": "kamus",
    "set": "himpunan",
    "NoneType": "kosong",
    "bytes": "data mentah",
    "bytearray": "larik byte",
    "range": "rentang",
    "complex": "angka kompleks",
    "function": "fungsi",
    "builtin_function_or_method": "fungsi bawaan",
    "module": "modul",
    "type": "kelas",
    "GeneratorType": "pembangkit (generator)",
}

def cetak_detail(nilai):
    """Menampilkan detail komprehensif dari objek yang dicetak, dalam Bahasa Indonesia."""

    waktu = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
    teks = str(nilai.nilai) if hasattr(nilai, "nilai") else str(nilai)
    tipe = type(nilai)
    tipe_nama = tipe.__name__
    tipe_id = TIPE_INDONESIA.get(tipe_nama, tipe_nama)
    modul = getattr(tipe, "__module__", "builtin")
    identitas = hex(id(nilai))
    hash_objek = hash(nilai) if isinstance(nilai, (str, int, float, bool, tuple)) else "tidak dapat dihitung"
    panjang = len(teks)
    ukuran = len(teks.encode("utf-8"))
    encoding = sys.getdefaultencoding()

    # Deteksi sifat objek
    is_builtin = modul == "builtins"
    is_callable = callable(nilai)
    is_iterable = hasattr(nilai, "__iter__")
    is_generator = isinstance(nilai, types.GeneratorType)
    jumlah_attr = len(vars(nilai)) if hasattr(nilai, "__dict__") else "tidak tersedia"

    # Preview isi
    if isinstance(nilai, (list, tuple, set)):
        jenis_isi = {type(i).__name__ for i in nilai} or {"kosong"}
        jenis_isi_id = {TIPE_INDONESIA.get(j, j) for j in jenis_isi}
        isi_preview = ", ".join(repr(i) for i in list(nilai)[:3])
        if len(nilai) > 3:
            isi_preview += ", ..."
        subtipe = f"berisi {', '.join(jenis_isi_id)}"
    elif isinstance(nilai, dict):
        k_tipe = type(next(iter(nilai.keys()), str)).__name__
        v_tipe = type(next(iter(nilai.values()), str)).__name__
        subtipe = f"berisi pasangan {TIPE_INDONESIA.get(k_tipe, k_tipe)} → {TIPE_INDONESIA.get(v_tipe, v_tipe)}"
        isi_preview = ", ".join(f"{k!r}: {v!r}" for k, v in list(nilai.items())[:3])
        if len(nilai) > 3:
            isi_preview += ", ..."
    else:
        subtipe = ""
        isi_preview = teks if len(teks) < 120 else teks[:300] + "..."

    # Info sistem
    os_info = platform.system()
    versi_os = platform.release()
    pengguna = getpass.getuser()
    python_ver = platform.python_version()

    # Cetak laporan
    print("\n" + "="*75)
    print(f"DETAIL OBJEK CETAK — {waktu}")
    print("-"*75)
    print(f"Jenis data       : {tipe_id} {subtipe}")
    print(f"Modul asal       : {modul} {'(bawaan)' if is_builtin else '(kustom)'}")
    print(f"Panjang teks     : {panjang} huruf | Ukuran: {ukuran} byte | Enkoding: {encoding}")
    print(f"Identitas objek  : {identitas} | Nilai hash: {hash_objek}")
    print(f"Dapat dipanggil  : {is_callable} | Dapat diulang: {is_iterable} | Pembangkit: {is_generator}")
    print(f"Jumlah atribut   : {jumlah_attr}")
    print("-"*75)
    print(f"Sistem operasi   : {os_info} {versi_os}")
    print(f"Versi Python     : {python_ver}")
    print(f"Pengguna aktif   : {pengguna}")
    print("-"*75)
    print(f"Cuplikan isi     : {isi_preview}")
    print("="*75 + "\n")
