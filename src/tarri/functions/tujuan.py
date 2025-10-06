# from .rute import ROUTES

# def tujuan(name: str) -> str:
#     """
#     Ambil URL dari nama rute.
#     - name bisa berupa nama rute ('/about', 'register', 'login')
#     - fungsi mencari di ROUTES dan mengembalikan URL
#     """
#     name = name.strip()

#     # jika sudah ada / di awal, anggap itu rute langsung
#     if name.startswith("/"):
#         if name in ROUTES:
#             return name
#         return "#"

#     # cari berdasarkan nama file
#     for url, target in ROUTES.items():
#         # cocokkan akhir file dengan name, tanpa folder
#         if target.endswith("/" + name) or target.endswith("/" + name + ".tarri") or target.endswith("/" + name + ".tarri.html"):
#             return url
#     return "#"


from .rute import ROUTES

def tujuan(name: str, *args) -> str:
    name = name.strip()

    # Ganti {1}, {2}, dst dengan args
    for i, arg in enumerate(args, start=1):
        name = name.replace(f"{{{i}}}", str(arg))

    # Jika sudah ada / di awal, langsung cocokkan
    if name.startswith("/"):
        for method, regex, _ in ROUTES:
            if regex.match(name):  # tidak batasi ke GET
                return name
        return "#"

    # Jika name adalah nama file, cari URL-nya
    for method, regex, target in ROUTES:
        if target.endswith("/" + name) or target.endswith("/" + name + ".tarri") or target.endswith("/" + name + ".tarri.html"):
            for test_url in ["/" + name, "/" + name + ".tarri", "/" + name + ".tarri.html"]:
                if regex.match(test_url):
                    return test_url
    return "#"
