#==============================================================================#
# File    : json.py                                                            #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'json' yang tersedia dalam bahasa Tarri.        #
#==============================================================================#

import json as json_modul


class TarriResponse:
    """
    Objek response internal Tarri
    Digunakan untuk bypass tataletak / layout
    """

    def __init__(
        self, body, content_type="text/html", status_code=200, tanpa_tataletak=False
    ):
        self.body = body
        self.content_type = content_type
        self.status_code = status_code
        self.tanpa_tataletak = tanpa_tataletak


def json(status="200", message="", data=None, meta=None, errors=None):
    """
    Standar JSON response untuk API TARRI
    - TIDAK dirender ke tataletak
    - Content-Type application/json
    """

    if meta is None:
        meta = {}

    if errors is None:
        errors = []

    payload = {
        "status": status,
        "message": message,
        "data": data,
        "meta": meta,
        "errors": errors,
    }

    body = json_modul.dumps(payload, indent=4, ensure_ascii=False)

    return TarriResponse(
        body=body,
        content_type="application/json",
        status_code=int(status) if str(status).isdigit() else 200,
        tanpa_tataletak=True,
    )
