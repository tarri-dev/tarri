#==============================================================================#
# File    : parse_json_api.py                                                  #
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

def parse_json_api(data, field_path):
    """
    Ambil nilai dari JSON berdasarkan path (misal: "data.user.nama").
    """
    if data is None:
        return None

    fields = field_path.split(".")
    result = data

    try:
        for f in fields:
            if isinstance(result, list):
                # Mendukung akses indeks list: "items.0.nama"
                try:
                    idx = int(f)
                    result = result[idx]
                except (ValueError, IndexError):
                    return None
            elif isinstance(result, dict):
                # Mengambil key dari dictionary
                result = result.get(f)
            else:
                return None

            # Jika di tengah jalan hasilnya None, langsung berhenti
            if result is None:
                break

        return result
    except (KeyError, IndexError, ValueError, TypeError):
        return None
