# # sesi.py
# _SESSION = {}

# def sesi(key=None, value=None):
#     """
#     Sesi global sederhana.
#     - sesi("key") -> ambil value
#     - sesi("key", value) -> set value
#     - sesi()->hapus("key") -> hapus key
#     - sesi()->semua() -> ambil semua session
#     """
#     global _SESSION

#     class SesiObj:
#         def ambil(self, k, default=None):
#             return _SESSION.get(k, default)

#         def simpan(self, k, v):
#             _SESSION[k] = v
#             return v

#         def hapus(self, k):
#             if k in _SESSION:
#                 del _SESSION[k]

#         def semua(self):
#             return dict(_SESSION)

#     s = SesiObj()

#     if key is None:
#         return s
#     if value is None:
#         return s.ambil(key)
#     else:
#         return s.simpan(key, value)


# # # set session
# # sesi("user", "Ketut Dana")

# # # ambil session
# # _nama = sesi("user")

# # # hapus session
# # sesi()->hapus("user")

# # # ambil semua session
# # _semua = sesi()->semua()


# sesi.py
class SesiObj:
    def __init__(self):
        self._data = {}

    def ambil(self, k, default=None):
        return self._data.get(k, default)

    def simpan(self, k, v):
        self._data[k] = v
        return v

    def hapus(self, k):
        if k in self._data:
            del self._data[k]

    def semua(self):
        return dict(self._data)

    def update(self, data: dict):
        """Tambahan: update semua key dari dict"""
        self._data.update(data)


# objek sesi global
_sesi_global = SesiObj()


def sesi(key=None, value=None):
    """
    Helper untuk akses sesi global:
      sesi("key") -> ambil value
      sesi("key", value) -> simpan
      sesi() -> objek sesi global
    """
    global _sesi_global
    if key is None:
        return _sesi_global
    if value is None:
        return _sesi_global.ambil(key)
    else:
        return _sesi_global.simpan(key, value)
