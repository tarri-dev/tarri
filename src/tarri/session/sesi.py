import os, json, uuid, time, socket, platform, locale
from pathlib import Path
from datetime import datetime

class SesiManager:
    EXPIRE_SECS = 86400  # 24 jam

    def __init__(self, lokasi=None, sesi_id=None, meta=None):
        self.tipe = "berkas"
        
        # Default folder sesi di ./sesi/
        default_dir = Path(os.getcwd()) / "sesi"
        self.lokasi = Path(lokasi or default_dir)
        os.makedirs(self.lokasi, exist_ok=True)

        # sesi_id unik per browser / client
        self.sesi_id = sesi_id or str(uuid.uuid4())
        self.file_path = self.lokasi / f"tarri_sesi_{self.sesi_id}.json"

        self.data = {}
        self._muat()

        now = time.time()
        meta = meta or {}
        defaults = {
            "sesi_id": {"value": self.sesi_id, "created": now},
            "_ip_private": {"value": self._get_private_ip(), "created": now},
            "_ip_public": {"value": meta.get("ip_public", "unknown"), "created": now},
            "_browser": {"value": meta.get("browser", "unknown"), "created": now},
            "_os": {"value": platform.system() + " " + platform.release(), "created": now},
            "_language": {"value": locale.getdefaultlocale()[0] or "unknown", "created": now},
            "_gmt": {"value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "created": now},
        }

        for k, v in defaults.items():
            if k not in self.data:
                self.data[k] = v

        self._simpan()


    # -------------------------------
    # Helper untuk ambil IP private
    # -------------------------------
    def _get_private_ip(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return "127.0.0.1"

    # ==============================
    # CONFIG / API
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

    def sesi_simpan(self, key, value):
        return self.perbarui({key: value})

    def sesi_ambil(self, key, default=None):
        return self.ambil(key, default)

    def sesi_hapus(self, key):
        return self.hapus(key)

    # ==============================
    # FILE UTIL
    # ==============================
    def _muat(self):
        if self.tipe != "berkas":
            return
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    now = time.time()
                    self.data = {}
                    for k, v in raw_data.items():
                        if isinstance(v, dict) and "created" in v and "value" in v:
                            if now - v["created"] <= self.EXPIRE_SECS:
                                self.data[k] = v
                        else:
                            self.data[k] = {"value": v, "created": now}
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
                    safe_data[k] = {"value": str(v), "created": time.time()}
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(safe_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[tarri | sesi] Gagal menyimpan sesi: {e}")

    # ==============================
    # AKSI SESI
    # ==============================
    def ambil(self, key, default=None):
        self._muat()
        k = self._unwrap(key)
        if k not in self.data:
            return default
        item = self.data[k]
        now = time.time()
        if now - item.get("created", now) > self.EXPIRE_SECS:
            self.hapus(k)
            return default
        return item.get("value", default)

    def semua(self):
        self._muat()
        now = time.time()
        hasil = {}
        for k, v in list(self.data.items()):
            if now - v.get("created", now) <= self.EXPIRE_SECS:
                hasil[k] = v.get("value")
            else:
                self.hapus(k)
        return hasil

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
        now = time.time()
        if isinstance(data, dict):
            cleaned = {}
            for k, v in data.items():
                key = self._unwrap(k)
                val = self._unwrap(v)
                cleaned[key] = {"value": val, "created": now}
            self.data.update(cleaned)
            self._simpan()
            return {k: v["value"] for k, v in cleaned.items()}
        else:
            self.data = {"value": self._unwrap(data), "created": now}
            self._simpan()
            return self.data["value"]

    # ==============================
    # INTERNAL
    # ==============================
    def _unwrap(self, v):
        try:
            if hasattr(v, "nilai"):
                return self._unwrap(v.nilai)
            if hasattr(v, "value"):
                return self._unwrap(v.value)
            if hasattr(v, "to_python"):
                return self._unwrap(v.to_python())
            if isinstance(v, list):
                return [self._unwrap(i) for i in v]
            if isinstance(v, dict):
                return {str(self._unwrap(k)): self._unwrap(val) for k, val in v.items()}
            return v
        except Exception:
            return str(v)

# =========================
# FUNGSI UTILITY
# =========================
def buat_sesi(browser_sesi_id=None, lokasi=None):
    """Buat instance SesiManager baru untuk tiap browser/client"""
    return SesiManager(lokasi=lokasi, sesi_id=browser_sesi_id)


# =========================
# API GLOBAL
# =========================
_sesi = SesiManager()  # fallback default
sesi = _sesi

def sesi_simpan(*args, **kwargs):
    data = {}
    if len(args) == 1 and isinstance(args[0], dict):
        data.update(args[0])
    elif len(args) >= 2:
        if len(args) % 2 != 0:
            raise ValueError("[tarri | sesi] Minimal pasangan dua argumen")
        for i in range(0, len(args), 2):
            k = _sesi._unwrap(args[i])
            v = _sesi._unwrap(args[i + 1])
            data[k] = v
    if kwargs:
        for k, v in kwargs.items():
            data[_sesi._unwrap(k)] = _sesi._unwrap(v)
    if not data:
        return {}
    hasil = _sesi.perbarui(data)
    _sesi._simpan()
    return hasil

def sesi_ambil(*args, default=None):
    if not args:
        return _sesi.semua()
    hasil = {k: _sesi.ambil(k, default) for k in args}
    if len(hasil) == 1:
        return list(hasil.values())[0]
    return hasil

def sesi_hapus(k):
    return _sesi.hapus(k)

def sesi_semua():
    return _sesi.semua()

def sesi_perbarui(data):
    return _sesi.perbarui(data)

def sesi_tipe(self, tipe=None):
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    if tipe:
        self.session.tipe = tipe
    return self.session.tipe

def sesi_lokasi(self, lokasi=None):
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    if lokasi:
        self.session.lokasi = Path(lokasi)
        os.makedirs(self.session.lokasi, exist_ok=True)
    return str(self.session.lokasi)
