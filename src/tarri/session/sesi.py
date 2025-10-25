import os, json, uuid
from pathlib import Path

class SesiManager:
    def __init__(self):
        self.tipe = "berkas"
        self.lokasi = Path(os.getcwd())
        self.data = {}
        self.file_path = self.lokasi / "tarri_sesi.json"
        self._muat()
        # Tambahkan sesi_id otomatis jika belum ada
        if "sesi_id" not in self.data:
            self.data["sesi_id"] = str(uuid.uuid4())
            self._simpan()

    # ==============================
    # KONFIGURASI
    # ==============================
    def set_tipe(self, tipe):
        if tipe not in ["berkas", "sistem"]:
            raise ValueError("Tipe sesi harus 'berkas' atau 'sistem'")
        self.tipe = tipe
        if tipe == "sistem":
            self.data = {}
        else:
            self._muat()
        return tipe

    def set_lokasi(self, path):
        if not path:
            path = os.getcwd()
        self.lokasi = Path(path)
        os.makedirs(self.lokasi, exist_ok=True)
        self.file_path = self.lokasi / "tarri_sesi.json"
        self._muat()
        # pastikan sesi_id tetap ada
        if "sesi_id" not in self.data:
            self.data["sesi_id"] = str(uuid.uuid4())
            self._simpan()
        return str(self.lokasi)

    # ==============================
    # UTILITAS FILE
    # ==============================
    def _muat(self):
        if self.tipe != "berkas":
            return
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def _simpan(self):
        if self.tipe != "berkas":
            return
        try:
            safe_data = {}
            for k, v in self.data.items():
                try:
                    json.dumps(v)
                    safe_data[k] = v
                except TypeError:
                    safe_data[k] = str(v)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(safe_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[tarri | sesi] gagal menyimpan sesi: {e}")

    # ==============================
    # AKSI SESI
    # ==============================

    def ambil(self, key, default=None):
        self._muat()
        return self.data.get(self._unwrap(key), default)

    def semua(self):
        self._muat()
        return dict(self.data)

    def hapus(self, key):
        self._muat()
        k = self._unwrap(key)
        if k in self.data:
            del self.data[k]
            self._simpan()
            return True
        return False

    def perbarui(self, data):
        self._muat()
        cleaned = {self._unwrap(k): self._unwrap(v) for k, v in data.items()}
        self.data.update(cleaned)
        self._simpan()
        return cleaned

    # ==============================
    # UTILITAS INTERNAL
    # ==============================
    def _unwrap(self, v):
        try:
            if hasattr(v, "nilai"):
                v = v.nilai
            elif hasattr(v, "value"):
                v = v.value
            elif hasattr(v, "to_python"):
                v = v.to_python()
        except Exception:
            pass
        if not isinstance(v, (str, int, float, bool, type(None), dict, list)):
            return str(v)
        return v


# ==============================================
# GLOBAL + HELPER UNTUK TARRI
# ==============================================
_sesi = SesiManager()


def sesi_tipe(tipe=None):
    return _sesi.set_tipe(tipe)


def sesi_lokasi(path=None):
    return _sesi.set_lokasi(path)


def sesi_simpan(*args, **kwargs):
    data = {}
    if args:
        if len(args) % 2 != 0:
            raise ValueError("Argumen posisi harus genap (pasangan kunci-nilai)")
        for i in range(0, len(args), 2):
            k = _sesi._unwrap(args[i])
            v = _sesi._unwrap(args[i + 1])
            data[k] = v

    for k, v in kwargs.items():
        data[_sesi._unwrap(k)] = _sesi._unwrap(v)

    return _sesi.perbarui(data)

def sesi_ambil(*args, default=None):
    if not args:
        return _sesi.semua()
    hasil = {k: _sesi.ambil(k, default) for k in args}
    if len(hasil) == 1:
        return list(hasil.values())[0]
    return ", ".join(f"{k}: {v}" for k, v in hasil.items())

def sesi_semua():
    return _sesi.semua()


def sesi_hapus(k):
    return _sesi.hapus(k)


def sesi_perbarui(data):
    return _sesi.perbarui(data)


def sesi(key=None, value=None, **kwargs):
    if key is None and not kwargs:
        return sesi_semua()
    if value is None and not kwargs:
        if isinstance(key, (list, tuple)):
            return {k: _sesi.ambil(k) for k in key}
        return _sesi.ambil(key)
    if kwargs:
        return sesi_simpan(key, value, **kwargs) if key else sesi_simpan(**kwargs)
    return sesi_simpan(key, value)
