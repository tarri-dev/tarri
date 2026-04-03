#==============================================================================#
# File    : sesi1.py                                                           #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Manajemen sesi pengguna, penyimpanan konteks sesi, dan pemulihan state     #
#   sesi Tarri.                                                                #
#==============================================================================#

import os, json, uuid, time, socket, platform, locale
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

# Global instance harus diinisialisasi hanya saat diakses
_GLOBAL_SESI: Optional["SesiManager"] = None


class SesiManager:
    EXPIRE_SECS = 86400  # 24 jam

    def __init__(
        self,
        lokasi: Optional[str] = None,
        sesi_id: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.tipe = "berkas"

        # Default folder sesi di ./sesi/
        default_dir = Path(os.getcwd()) / "sesi"
        self.lokasi = Path(lokasi or default_dir)
        os.makedirs(self.lokasi, exist_ok=True)

        # sesi_id unik per browser / client. Jika None, ID baru dibuat.
        self.sesi_id = sesi_id or str(uuid.uuid4())
        self.file_path = self.lokasi / f"tarri_sesi_{self.sesi_id}.json"

        self.data = {}

        # 🎯 Perbaikan 1: Cek apakah file sesi sudah ada.
        file_ditemukan = self._muat()

        # Jika file ditemukan, _muat() sudah mengisi self.data.
        # Jika file TIDAK ditemukan (inisialisasi baru, termasuk saat worker startup),
        # kita isi metadata dan TIDAK menyimpan ke disk.
        if not file_ditemukan:
            self._set_default_metadata(meta)
            # self._simpan() Dihapus di sini. Sesi hanya disimpan saat data diubah.

    # -------------------------------
    # Helper untuk set default metadata
    # -------------------------------
    def _set_default_metadata(self, meta: Optional[Dict[str, Any]]):
        """Mengisi metadata default hanya saat sesi baru dibuat."""
        now = time.time()
        meta = meta or {}
        defaults = {
            "sesi_id": {"value": self.sesi_id, "created": now},
            "_ip_private": {"value": self._get_private_ip(), "created": now},
            "_ip_public": {"value": meta.get("ip_public", "unknown"), "created": now},
            "_browser": {"value": meta.get("browser", "unknown"), "created": now},
            "_os": {
                "value": platform.system() + " " + platform.release(),
                "created": now,
            },
            "_language": {
                "value": locale.getdefaultlocale()[0] or "unknown",
                "created": now,
            },
            "_gmt": {
                "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "created": now,
            },
        }

        for k, v in defaults.items():
            if k not in self.data:
                self.data[k] = v

    # -------------------------------
    # Helper untuk ambil IP private
    # -------------------------------
    def _get_private_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
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
        # Dipakai oleh API global, akan dipanggil dari sesi_hapus global yang baru
        return self.hapus(key)

    # ==============================
    # FILE UTIL
    # ==============================
    def _muat(self) -> bool:
        """Memuat sesi dari file. Mengembalikan True jika file ditemukan."""
        if self.tipe != "berkas":
            return False

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
                            # Kompatibilitas mundur untuk data lama
                            self.data[k] = {"value": v, "created": now}
                    return True  # File ditemukan dan berhasil dimuat
            except Exception:
                self.data = {}
                return False
        return False  # File tidak ditemukan

    def _simpan(self):
        """Menyimpan sesi ke file hanya jika ada data pengguna yang sah."""
        if self.tipe != "berkas":
            return

        # 🎯 Perbaikan 2: Cek data. Hapus kunci metadata yang diawali underscore, kecuali 'sesi_id'
        data_user_saja = {
            k: v
            for k, v in self.data.items()
            if not k.startswith("_") or k == "sesi_id"
        }

        # Hanya simpan jika ada data selain metadata default ('sesi_id' pasti ada)
        if len(data_user_saja) <= 1:
            # Jika tidak ada data pengguna, hapus file lama (jika ada) dan keluar.
            if self.file_path.exists():
                try:
                    os.remove(self.file_path)
                except Exception as e:
                    print(f"[tarri | sesi] Gagal menghapus sesi kosong: {e}")
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
    def hancurkan(self) -> bool:
        global _GLOBAL_SESI  # Tambahkan ini agar bisa mereset variabel global
        try:
            # 1. Hapus file fisik
            if self.file_path.exists():
                os.remove(self.file_path)

            # 2. Kosongkan data di memori objek ini
            self.data = {}

            # 3. RESET TOTAL: Paksa instance global menjadi None
            # Dengan begini, panggilan sesi berikutnya akan dipaksa buat instance baru yang kosong
            _GLOBAL_SESI = None

            return True
        except Exception as e:
            print(f"[tarri | sesi] Gagal total menghancurkan sesi: {e}")
            return False

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

    def hapus(self, key: Union[str, List[str]]):
        """
        Menghapus satu kunci (string) atau banyak kunci (list/array) dari sesi.
        Mengembalikan True jika setidaknya satu kunci berhasil dihapus, False jika tidak ada.
        """
        self._muat()
        keys_to_delete: List[str] = []

        # 1. Tentukan kunci yang akan dihapus
        unwrapped_key = self._unwrap(key)

        if isinstance(unwrapped_key, (list, tuple)):
            # Jika array/list diterima (setelah unwrap)
            keys_to_delete.extend(unwrapped_key)
        else:
            # Jika string tunggal diterima
            keys_to_delete.append(str(unwrapped_key))

        # 2. Lakukan penghapusan
        keys_deleted_count = 0
        for k in keys_to_delete:
            if k in self.data:
                del self.data[k]
                keys_deleted_count += 1

        # 3. Simpan perubahan hanya jika ada yang terhapus
        if keys_deleted_count > 0:
            self._simpan()
            return True

        # 4. Gagal (tidak ada yang ditemukan/dihapus)
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
                # PERHATIAN: ini akan mengembalikan list Python, yang akan ditangani
                # oleh logika di metode hapus()
                return [self._unwrap(i) for i in v]
            if isinstance(v, dict):
                return {str(self._unwrap(k)): self._unwrap(val) for k, val in v.items()}
            return v
        except Exception:
            return str(v)


# =========================
# FUNGSI UTILITY
# =========================
def buat_sesi(
    browser_sesi_id: Optional[str] = None, lokasi: Optional[str] = None
) -> SesiManager:
    """Buat instance SesiManager baru untuk tiap browser/client"""
    return SesiManager(lokasi=lokasi, sesi_id=browser_sesi_id)


# =========================
# API GLOBAL (Perbaikan dengan Lazy Initialization)
# =========================


def sesi_hancurkan():
    """API Global untuk menghancurkan sesi yang sedang aktif."""
    _sesi = _get_global_sesi()
    return _sesi.hancurkan()


def _get_global_sesi() -> SesiManager:
    """Menginisialisasi sesi global (untuk API) hanya saat diakses."""
    global _GLOBAL_SESI
    if _GLOBAL_SESI is None:
        # Inisialisasi sesi fallback. ID dibuat, tapi file tidak akan ditulis ke disk.
        _GLOBAL_SESI = SesiManager()
    return _GLOBAL_SESI


# Hapus baris _sesi = SesiManager() dan sesi = _sesi dari versi lama.
# Gunakan fungsi _get_global_sesi() di setiap fungsi API di bawah.


def sesi_simpan(*args, **kwargs):
    _sesi = _get_global_sesi()
    data: Dict[str, Any] = {}
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
    return _sesi.perbarui(data)


def sesi_ambil(*args, default=None):
    _sesi = _get_global_sesi()
    sesi_id = _sesi.ambil("sesi_id")

    if sesi_id:
        folder_sesi = Path(os.getcwd()) / "sesi"
        file_sesi = folder_sesi / f"{sesi_id}.json"

        # VALIDASI KRUSIAL UNTUK WORKER
        if not file_sesi.exists():
            # Jika file sudah dihapus worker lain, bersihkan memori lokal worker ini
            _sesi.data = {}
            return default if len(args) == 1 else {k: default for k in args}

    # Lanjutkan ambil data dari memori yang sudah terverifikasi
    if not args:
        return _sesi.semua()

    hasil = {k: _sesi.ambil(k, default) for k in args}
    return list(hasil.values())[0] if len(args) == 1 else hasil


def sesi_hapus(k: Union[str, List[str]]):
    """
    Menghapus kunci sesi. Menerima string tunggal atau list/array string.
    Mengembalikan True jika sukses, False jika gagal.
    """
    _sesi = _get_global_sesi()
    # Meneruskan k langsung ke metode hapus yang sudah mendukung string atau list
    return _sesi.hapus(k)


def sesi_semua():
    _sesi = _get_global_sesi()
    return _sesi.semua()


def sesi_perbarui(data):
    _sesi = _get_global_sesi()
    return _sesi.perbarui(data)


def sesi_tipe(self, tipe=None):
    # Asumsi self.session diatur oleh interpreter Tarri, bukan sesi global
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    if tipe:
        self.session.tipe = tipe
    return self.session.tipe


def sesi_lokasi(self, lokasi=None):
    # Asumsi self.session diatur oleh interpreter Tarri, bukan sesi global
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    if lokasi:
        self.session.lokasi = Path(lokasi)
        os.makedirs(self.session.lokasi, exist_ok=True)
    return str(self.session.lokasi)


# =========================
# API GLOBAL (lanjutan)
# =========================

# Tambahkan alias sesi agar modul lain bisa mengimpornya
sesi = _get_global_sesi()
