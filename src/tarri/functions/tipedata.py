def tipedata(val):
    """Mengembalikan nama tipe data dalam bahasa Indonesia"""
    # CEK BOOLEAN DULU!
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, int):
        return "angka"
    elif isinstance(val, float):
        return "desimal"
    elif isinstance(val, str):
        return "kata"
    elif val is None:
        return "kosong"
    else:
        return "tidak diketahui"
