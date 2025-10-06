# tarri/functions/rute.py

# ROUTES = {}

# def rute(url_path: str, target: str):
#     """
#     Daftarkan rute aplikasi.
#     - url_path: path di browser, contoh "/register"
#     - target: file tujuan relatif dari ROOT_PROJECT
#     """
#     global ROUTES   # <--- ini penting
#     url_path = url_path.strip()
#     target = target.strip()
#     ROUTES[url_path] = target
#     return ""  # supaya tidak tampil di output


import re

# ROUTES: list of (method, regex, target)
ROUTES = []

def rute(url_path: str, target: str, method="GET"):
    """
    Daftarkan rute aplikasi.
    - url_path: path di browser, contoh "/register" atau "/pengguna/{id}"
    - target: file tujuan relatif dari ROOT_PROJECT
    - method: "GET" atau "POST"
    """
    url_path = url_path.strip()
    target = target.strip()
    method = method.upper()

    # Ubah {param} → regex grup: "([^/]+)"
    pattern = re.sub(r"\{[^\}]+\}", r"([^/]+)", url_path)
    regex = re.compile(f"^{pattern}$")

    ROUTES.append((method, regex, target))
    return ""

