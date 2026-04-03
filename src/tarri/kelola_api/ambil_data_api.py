#==============================================================================#
# File    : ambil_data_api.py                                                  #
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
import logging
import os
from pathlib import Path

logger = logging.getLogger("tarriserver.api_client")


def _muat_konfigurasi_manual():
    """Membaca .tarri.conf dari root project secara mandiri."""
    conf_path = Path(os.getcwd()) / ".tarri.conf"
    if not conf_path.exists():
        return {}

    data = {}
    section = None
    try:
        for line in conf_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip()
                data[section] = {}
            elif "=" in line and section is not None:
                key, val = map(str.strip, line.split("=", 1))
                data[section][key] = val
        return data
    except Exception:
        return {}


def ambil_data_api(
    url,
    _sumber="api_url",
    headers=None,
    halaman=None,
    batas=None,
    params=None,
    context=None,
):
    """
    Urutan parameter baru:
    1. url
    2. _sumber (Pindah ke sini agar mudah dipanggil dari .tarri)
    3. headers
    ... dst
    """
    # 1. Tentukan Base URL Awal
    base_url = "http://127.0.0.1:8000"

    # Muat konfigurasi
    conf = {}
    if context and hasattr(context, "config") and context.config:
        conf = context.config
    else:
        conf = _muat_konfigurasi_manual()

    # 2. Ambil Base URL dari .tarri.conf berdasarkan _sumber
    if conf and "server" in conf:
        base_url = conf["server"].get(_sumber, base_url)

    # 3. Bangun URL Final
    if url.startswith("http"):
        full_url = url
    else:
        path_bersih = url.lstrip("/")
        full_url = f"{base_url.rstrip('/')}/{path_bersih}"

    # 4. Preparasi Headers & Sesi Otomatis
    request_headers = {
        "Accept": "application/json",
        "User-Agent": "TarriFramework/2.0",
        "Connection": "close",
    }

    # Sesi otomatis tetap berjalan di latar belakang
    if headers is None and context and hasattr(context, "session"):
        try:
            sesi_id = context.session.ambil("sesi_id")
            if sesi_id:
                request_headers["Cookie"] = f"sesi_id={sesi_id}"
        except Exception:
            pass
    elif isinstance(headers, dict):
        request_headers.update(headers)

    # 5. Eksekusi Request
    try:
        query_params = {} if params is None else dict(params)
        if halaman:
            query_params["_page"] = halaman
        if batas:
            query_params["_limit"] = batas

        res = requests.get(
            full_url, params=query_params, headers=request_headers, timeout=5
        )

        if res.status_code != 200:
            logger.warning(f"API Response {res.status_code}: {full_url}")

        if "application/json" in res.headers.get("Content-Type", ""):
            return res.json()

        return {"status": res.status_code, "content": res.text}

    except requests.exceptions.RequestException as e:
        logger.error(f"Gagal koneksi API ke {full_url}: {str(e)}")
        return {"status": 500, "message": str(e)}
