#==============================================================================#
# File    : alihkan.py                                                         #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'alihkan' yang tersedia dalam bahasa Tarri.     #
#==============================================================================#

try:
    from fastapi.responses import RedirectResponse
except ImportError:
    RedirectResponse = None


def alihkan(interpreter, target, data=None, status_code: int = 302):

    # === Normalisasi target ===
    if isinstance(target, (list, tuple)):
        path = str(target[0]).strip()
        if len(target) > 1 and data is None:
            data = target[1]
    else:
        path = str(target).strip()

    # === Validasi dasar ===
    if not path:
        print("[tarri | alihkan] Path kosong, redirect dibatalkan.")
        return

    # === Simpan data ke sesi (jika ada) ===
    sesi = getattr(interpreter, "session", None)
    if sesi and data:
        # simpan data dengan nama khusus agar bisa diambil GET berikutnya
        try:
            if not isinstance(data, dict):
                data = {"_pesan": str(data)}  # bungkus otomatis jadi dict
            sesi.perbarui({"_redirect_data": data})
        except Exception as e:
            print(f"[tarri | alihkan] Gagal menyimpan data redirect ke sesi: {e}")

    # === Log internal ===
    print(f"[tarri | alihkan] Alihkan ke: {path}, dengan data: {data}")

    # === Kembalikan response redirect ===
    raise StopIteration(RedirectResponse(url=path, status_code=status_code))
