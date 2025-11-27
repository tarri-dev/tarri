# kelola_api/hapus_data_api.py
import requests

def hapus_data_api(url, headers=None):
    """
    Menghapus data di API menggunakan metode DELETE.
    - url: endpoint API (misal https://.../posts/1)
    - headers: dictionary header opsional
    """
    try:
        res = requests.delete(url, headers=headers, timeout=10)
        res.raise_for_status()
        return True  # berhasil
    except requests.exceptions.RequestException:
        return False
