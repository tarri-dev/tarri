#==============================================================================#
# File    : simpan_data_api.py                                                 #
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

import json
import os


def simpan_data_api(data, filename="data_api.json", folder="data"):
    """
    Simpan data (dict/list) ke file JSON lokal.
    """
    # 1. Pastikan folder ada
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception as e:
        return f"Gagal membuat folder: {str(e)}"

    filepath = os.path.join(folder, filename)

    # 2. Validasi data sebelum disimpan
    if data is None:
        return "Gagal: Data yang ingin disimpan kosong (None)."

    try:
        # 3. Proses tulis file
        with open(filepath, "w", encoding="utf-8") as f:
            # Gunakan indent=4 agar file JSON enak dibaca manusia
            json.dump(data, f, indent=4, ensure_ascii=False)

        return filepath  # Mengembalikan path file sebagai bukti sukses
    except Exception as e:
        return f"Error menyimpan data: {str(e)}"
