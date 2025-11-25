# tarri/functions/tujuan.py
def tujuan(name: str, *args) -> str:
    """
    Versi ringan: hanya mengembalikan path absolut atau relatif.
    Tidak lagi bergantung pada ROUTES.
    """
    if not name:
        return "#"

    # Ganti {1}, {2}, dst dengan args (untuk dinamis)
    for i, arg in enumerate(args, start=1):
        name = name.replace(f"{{{i}}}", str(arg))

    # Jika sudah berupa path absolut
    if name.startswith("/"):
        return name

    # Jika bukan path, anggap sebagai nama fungsi atau file
    return f"/{name.strip()}"
