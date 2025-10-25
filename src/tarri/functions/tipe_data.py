def tipe_data(val):
    """Mengembalikan nama tipe data dalam bahasa Indonesia"""
    # Urutan penting, agar tidak salah deteksi
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, int):
        return "angka"
    elif isinstance(val, float):
        return "desimal"
    elif isinstance(val, str):
        return "kata"
    elif isinstance(val, list):
        return "daftar"
    elif isinstance(val, dict):
        return "objek"
    elif isinstance(val, tuple):
        return "kumpulan"
    elif isinstance(val, set):
        return "himpuan"
    elif val is None:
        return "kosong"
    else:
        return "tidak diketahui"
