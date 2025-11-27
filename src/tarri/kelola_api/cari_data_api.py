# kelola_api/ambil_data_api.py
def cari_data_api(data, **kwargs):
    """
    Cari item dalam list/dictionary berdasarkan key=value.
    - data: list of dict (hasil dari ambil_data_api)
    - kwargs: key=value yang dicari
    Return list item yang cocok.
    """
    if not isinstance(data, list):
        return []

    hasil = []
    for item in data:
        cocok = True
        for k, v in kwargs.items():
            # jika key tidak ada atau value tidak sama, skip
            if k not in item or item[k] != v:
                cocok = False
                break
        if cocok:
            hasil.append(item)
    return hasil
