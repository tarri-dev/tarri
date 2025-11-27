# kelola_api/perbarui_data_api.py
import requests

def perbarui_data_api(url, data, headers=None):
    """
    Memperbarui data di API menggunakan metode PUT.
    - url: endpoint API (misal https://.../posts/1)
    - data: dictionary data yang ingin diperbarui
    - headers: dictionary header opsional
    """
    try:
        res = requests.put(url, json=data, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException:
        return None
