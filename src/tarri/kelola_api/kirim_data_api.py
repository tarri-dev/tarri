import requests


def kirim_data_api(url: str, data: dict, headers: dict | None = None):
    """
    Mengirim data ke API menggunakan metode POST.

    Parameters:
        url (str): Endpoint API.
        data (dict): Data yang akan dikirim.
        headers (dict|None): Header tambahan jika diperlukan.

    Returns:
        dict: Response JSON jika valid, atau dict berisi error.
    """
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return {
            "sukses": True,
            "status": response.status_code,
            "data": response.json(),
        }
    except requests.exceptions.RequestException as e:
        return {
            "sukses": False,
            "error": str(e),
        }