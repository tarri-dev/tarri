def urutkan_data(self, args):
    if not args:
        return []

    data = args[0]
    arah = args[1] if len(args) > 1 else None  # bisa None atau indikator

    if data is None or not isinstance(data, list):
        return data

    # List angka
    if all(isinstance(i, (int, float)) for i in data):
        # Default membesar
        if arah is None:
            arah = "0-9"
        reverse = str(arah).strip().lower() in ("9-0", "mengecil")
        return sorted(data, reverse=reverse)

    # List string/huruf
    elif all(isinstance(i, str) for i in data):
        # Default membesar
        if arah is None:
            arah = "a-z"
        reverse = str(arah).strip().lower() in ("z-a", "mengecil")
        return sorted(data, reverse=reverse)

    # List campuran atau tipe lain
    return data
