#==============================================================================#
# File    : cari_data_api.py                                                   #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Komponen internal bahasa pemrograman Tarri.                                #
#==============================================================================#

def cari_data_api(data, **kwargs):
    """
    Cari item dalam list of dictionary berdasarkan key=value.
    Mendukung pencarian string yang tidak sensitif huruf besar/kecil.
    """
    # Pastikan data adalah list (biasanya dari _res["data"])
    if not isinstance(data, list):
        # Jika dikirim dict yang punya key 'data', otomatis ambil isinya
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        else:
            return []

    if not kwargs:
        return data

    hasil = []
    for item in data:
        if not isinstance(item, dict):
            continue

        cocok = True
        for k, v in kwargs.items():
            # Jika key tidak ada, langsung gagal
            if k not in item:
                cocok = False
                break

            val_item = item[k]

            # Normalisasi pencarian string (Case Insensitive)
            if isinstance(val_item, str) and isinstance(v, str):
                if val_item.lower() != v.lower():
                    cocok = False
                    break
            else:
                # Untuk tipe data lain (int, bool, dll)
                if val_item != v:
                    cocok = False
                    break

        if cocok:
            hasil.append(item)

    return hasil
