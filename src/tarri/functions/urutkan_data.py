def urutkan_data(self, args):
    if not args:
        return []

    data = args[0]
    arah = args[1] if len(args) > 1 else "membesar"

    if data is None or not isinstance(data, list):
        return data

    reverse = (str(arah).strip().lower() == "mengecil")

    # Hanya urut list 1D berisi angka
    if all(isinstance(i, (int, float)) for i in data):
        return sorted(data, reverse=reverse)

    return data
