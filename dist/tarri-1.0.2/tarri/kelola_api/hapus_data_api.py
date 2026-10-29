#==============================================================================#
# File    : hapus_data_api.py                                                  #
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


def hapus_data_api(url, headers=None, context=None):
    """
    Menghapus data di API menggunakan metode DELETE dengan dukungan sesi otomatis.
    """
    request_headers = {"Accept": "application/json", "User-Agent": "TarriFramework/2.0"}

    # OTOMATISASI SESI
    if headers is None and context is not None:
        if hasattr(context, "session"):
            try:
                sesi_id = context.session.ambil("sesi_id")
                if sesi_id:
                    request_headers["Cookie"] = f"sesi_id={sesi_id}"
            except:
                pass

    # Jika ada header manual, gabungkan
    if isinstance(headers, dict):
        request_headers.update(headers)

    try:
        # Eksekusi DELETE
        res = requests.delete(url, headers=request_headers, timeout=10)

        # Berhasil jika status 200 (OK) atau 204 (No Content)
        return 200 <= res.status_code < 300

    except requests.exceptions.RequestException:
        return False
