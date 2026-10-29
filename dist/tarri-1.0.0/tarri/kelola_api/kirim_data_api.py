#==============================================================================#
# File    : kirim_data_api.py                                                  #
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


def kirim_data_api(url: str, data: dict, headers: dict | None = None, context=None):
    """
    Mengirim data ke API menggunakan metode POST dengan otomatisasi sesi.
    """
    # 1. Siapkan Default Headers
    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "TarriFramework/2.0",
    }

    # 2. OTOMATISASI SESI: Ambil dari context jika headers manual tidak ada
    if headers is None and context is not None:
        if hasattr(context, "session"):
            try:
                sesi_id = context.session.ambil("sesi_id")
                if sesi_id:
                    request_headers["Cookie"] = f"sesi_id={sesi_id}"
            except:
                pass

    # Jika ada headers manual (dict), gabungkan
    if isinstance(headers, dict):
        request_headers.update(headers)
    # Jika headers dikirim berupa string (shortcut sesi_id)
    elif isinstance(headers, str):
        request_headers["Cookie"] = f"sesi_id={headers}"

    try:
        # 3. Eksekusi POST
        response = requests.post(url, json=data, headers=request_headers, timeout=10)

        # 4. Tangani Respon
        if "application/json" in response.headers.get("Content-Type", ""):
            return {
                "sukses": True,
                "status": response.status_code,
                "data": response.json(),
            }
        else:
            return {
                "sukses": response.status_code < 400,
                "status": response.status_code,
                "content": response.text,
            }

    except requests.exceptions.RequestException as e:
        return {
            "sukses": False,
            "status": 500,
            "error": str(e),
        }
