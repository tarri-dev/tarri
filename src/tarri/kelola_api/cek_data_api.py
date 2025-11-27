import requests

def cek_data_api(url, timeout=5):
    """
    Mengecek apakah API bisa diakses.
    Return True jika status code 200–399, False jika error atau timeout.
    """
    try:
        res = requests.get(url, timeout=timeout)
        if 200 <= res.status_code < 400:
            return True
        return False
    except requests.exceptions.RequestException:
        return False
