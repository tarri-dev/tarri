def ubah_kata(x):
    """
    Mengubah apapun menjadi string dengan aman.

    - None → ""
    - List/Dict → representasi JSON
    - Semua tipe lain → str()
    """
    import json

    if x is None:
        return ""
    elif isinstance(x, (list, dict)):
        try:
            return json.dumps(x, ensure_ascii=False)
        except Exception:
            return str(x)
    else:
        return str(x)
