# cari_data.py

def cari_data(interpreter, args):
    """
    Cari data di list of dict dan kembalikan:
    - 1 hasil → string
    - >1 hasil → list
    """
    data_list = args[0]
    prompt = args[1] if len(args) > 1 else "Masukkan kata kunci"

    print(f"\n{prompt}")
    keyword = input("> ").strip()

    if not keyword:
        print(f"[tarri | cari_data] Anda belum memasukkan data pencarian!")
        return None  # hentikan fungsi

    hasil = []
    for item in data_list:
        if not isinstance(item, dict):
            continue
        for k, v in item.items():
            if isinstance(v, str) and keyword.lower() in v.lower():
                hasil.append(v)

    if not hasil:
        print(f"[tarri | cari_data] data yang kamu cari '{keyword}' tidak ditemukan!")
        return None

    # adaptif: 1 hasil → string, lebih dari 1 → list
    if len(hasil) == 1:
        return hasil[0]
    else:
        return hasil
