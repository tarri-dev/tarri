#==============================================================================#
# File    : perbarui_data_api.py                                               #
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


def perbarui_data_api(url, data, headers=None, context=None):
    """
    Memperbarui data di API menggunakan metode PUT dengan dukungan sesi otomatis.
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
                # Mengambil sesi_id dari session manager
                sesi_id = context.session.ambil("sesi_id")
                if sesi_id:
                    request_headers["Cookie"] = f"sesi_id={sesi_id}"
            except:
                pass

    # Gabungkan jika ada headers manual (dict)
    if isinstance(headers, dict):
        request_headers.update(headers)

    try:
        # 3. Eksekusi PUT
        res = requests.put(url, json=data, headers=request_headers, timeout=10)

        # 4. Tangani Respon
        if "application/json" in res.headers.get("Content-Type", ""):
            return res.json()

        # Jika bukan JSON (misal sukses tapi return text), kembalikan status dan text
        return {"status": res.status_code, "content": res.text}

    except requests.exceptions.RequestException as e:
        return {"status": 500, "message": str(e)}
