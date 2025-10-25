def cari_data(interpreter, args):
    """
    Cari data di list atau list of dict dan kembalikan:
    - 1 hasil → string atau angka (tanpa tanda kutip)
    - >1 hasil → list campuran string/angka
    """
    data_list = args[0]
    prompt = args[1] if len(args) > 1 else "Masukkan kata kunci"

    print(f"\n{prompt}")
    keyword = input("> ").strip()

    if not keyword:
        print(f"[tarri | cari_data] Anda belum memasukkan data pencarian!")
        return None

    hasil = []

    for item in data_list:
        # jika dict → cek setiap value
        if isinstance(item, dict):
            for v in item.values():
                if isinstance(v, str) and keyword.lower() in v.lower():
                    hasil.append(v)
                elif not isinstance(v, str) and keyword in str(v):
                    # kembalikan angka tanpa kutip
                    hasil.append(v)
        else:
            # array biasa → langsung cek item
            if isinstance(item, str) and keyword.lower() in item.lower():
                hasil.append(item)
            elif not isinstance(item, str) and keyword in str(item):
                hasil.append(item)

    if not hasil:
        print(f"[tarri | cari_data] Data yang kamu cari '{keyword}' tidak ditemukan!")
        return None

    # adaptif: 1 hasil → langsung nilai, >1 → list
    return hasil[0] if len(hasil) == 1 else hasil
