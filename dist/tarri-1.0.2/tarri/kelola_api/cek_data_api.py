#==============================================================================#
# File    : cek_data_api.py                                                    #
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

import requests


def cek_data_api(url, timeout=5, context=None):
    """
    Mengecek apakah API bisa diakses (dengan dukungan otomatisasi sesi).
    """
    request_headers = {"Accept": "application/json", "User-Agent": "TarriFramework/2.0"}

    # OTOMATISASI SESI: Ambil dari context jika ada
    if context and hasattr(context, "session"):
        try:
            sesi_id = context.session.ambil("sesi_id")
            if sesi_id:
                request_headers["Cookie"] = f"sesi_id={sesi_id}"
        except:
            pass

    try:
        # Kirim request dengan header yang sudah berisi cookie (jika ada)
        res = requests.get(url, headers=request_headers, timeout=timeout)

        # API dianggap "tersedia" jika sukses (200-399)
        return 200 <= res.status_code < 400

    except requests.exceptions.RequestException:
        return False
