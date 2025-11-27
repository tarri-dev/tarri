# kelola_api/ambil_data_api.py
import requests

def ambil_data_api(url, halaman=None, batas=None, params=None, headers=None):
    """
    Ambil data dari API.
    - url: URL API
    - halaman: opsional, nomor halaman
    - batas: opsional, batas jumlah data per halaman
    - params: dictionary tambahan query params
    - headers: dictionary header
    """

    # Gabungkan params opsional
    query_params = {} if params is None else dict(params)  # salin supaya aman
    if halaman is not None:
        query_params["_page"] = halaman
    if batas is not None:
        query_params["_limit"] = batas

    try:
        res = requests.get(url, params=query_params, headers=headers, timeout=10)
        res.raise_for_status()  # akan raise exception jika status != 200
        return res.json()
    except requests.exceptions.RequestException:
        return None
