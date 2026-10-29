#==============================================================================#
# File    : sesi.py                                                            #
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

import os
import json
import uuid
import time
import socket
import platform
import locale
import fcntl  # 🆕 Import file locking (Unix/Mac)
import hashlib  # 🆕 Untuk hash session
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import threading  # 🆕 Untuk thread-safe operations

# Global instance harus diinisialisasi hanya saat diakses
_GLOBAL_SESI: Optional["SesiManager"] = None

# 🆕 Lock global untuk mencegah race condition di level modul
_MODULE_LOCK = threading.RLock()


class SesiManager:
    EXPIRE_SECS = 86400  # 24 jam

    def __init__(
        self,
        lokasi: Optional[str] = None,
        sesi_id: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        # 🆕 Gunakan lock untuk instance ini
        self._lock = threading.RLock()

        self.tipe = "berkas"

        # Default folder sesi di ./sesi/
        default_dir = Path(os.getcwd()) / "sesi"
        self.lokasi = Path(lokasi or default_dir)
        os.makedirs(self.lokasi, exist_ok=True)

        # sesi_id unik per browser / client. Jika None, ID baru dibuat.
        self.sesi_id = sesi_id or self._generate_session_id()
        self.file_path = self.lokasi / f"tarri_sesi_{self.sesi_id}.json"

        # 🆕 Lock file untuk session ini
        self.lock_file = self.lokasi / f"tarri_sesi_{self.sesi_id}.lock"

        self.data = {}

        # 🆕 Perbaikan: Gunakan locking saat load
        file_ditemukan = self._muat_dengan_lock()

        # Jika file ditemukan, _muat_dengan_lock() sudah mengisi self.data.
        # Jika file TIDAK ditemukan (inisialisasi baru, termasuk saat worker startup),
        # kita isi metadata dan TIDAK menyimpan ke disk.
        if not file_ditemukan:
            self._set_default_metadata(meta)

    # 🆕 Method baru: Generate session ID dengan hash untuk unikness
    def _generate_session_id(self) -> str:
        """Generate secure session ID dengan timestamp dan random"""
        import secrets

        timestamp = str(time.time_ns())
        random_part = secrets.token_hex(8)
        combined = f"{timestamp}_{random_part}"
        return hashlib.sha256(combined.encode()).hexdigest()[:32]

    # -------------------------------
    # Helper untuk set default metadata
    # -------------------------------
    def _set_default_metadata(self, meta: Optional[Dict[str, Any]]):
        """Mengisi metadata default hanya saat sesi baru dibuat."""
        with self._lock:
            now = time.time()
            meta = meta or {}
            defaults = {
                "sesi_id": {"value": self.sesi_id, "created": now},
                "_ip_private": {"value": self._get_private_ip(), "created": now},
                "_ip_public": {
                    "value": meta.get("ip_public", "unknown"),
                    "created": now,
                },
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

    # 🆕 File locking helpers
    def _acquire_file_lock(self):
        """Acquire file lock untuk session ini"""
        try:
            # Buat lock file
            self.lock_fd = open(self.lock_file, "w")
            # Gunakan flock untuk Unix/Mac
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX)
            return True
        except Exception as e:
            # Fallback ke file existence check untuk Windows/fallback
            try:
                # Coba buat lock file sebagai marker
                with open(self.lock_file, "w") as f:
                    f.write(str(os.getpid()))
                return True
            except:
                print(
                    f"[tarri | sesi] Gagal acquire lock untuk {self.sesi_id[:10]}: {e}"
                )
                return False

    def _release_file_lock(self):
        """Release file lock"""
        try:
            if hasattr(self, "lock_fd"):
                try:
                    fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                except:
                    pass
                self.lock_fd.close()

            # Hapus lock file
            if self.lock_file.exists():
                self.lock_file.unlink()
        except Exception:
            pass

    # ==============================
    # CONFIG / API
    # ==============================
    def set_tipe(self, tipe):
        with self._lock:
            if tipe not in ["berkas", "sistem"]:
                raise ValueError("Tipe sesi harus 'berkas' atau 'sistem'")
            self.tipe = tipe
            if tipe == "sistem":
                self.data = {}
            else:
                self._muat_dengan_lock()
            return tipe

    def sesi_simpan(self, key, value):
        return self.perbarui({key: value})

    def sesi_ambil(self, key, default=None):
        return self.ambil(key, default)

    def sesi_hapus(self, key):
        return self.hapus(key)

    # ==============================
    # FILE UTIL DENGAN LOCKING
    # ==============================
    def _muat_dengan_lock(self) -> bool:
        """Memuat sesi dari file dengan locking."""
        if self.tipe != "berkas":
            return False

        acquired = self._acquire_file_lock()
        if not acquired:
            # Jika gagal acquire lock, tunggu sebentar dan coba lagi
            time.sleep(0.01)
            acquired = self._acquire_file_lock()
            if not acquired:
                return False

        try:
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
                        return True
                except Exception as e:
                    print(f"[tarri | sesi] Gagal membaca sesi {self.sesi_id[:10]}: {e}")
                    self.data = {}
                    return False
            return False
        finally:
            self._release_file_lock()

    def _simpan_dengan_lock(self):
        """Menyimpan sesi ke file dengan locking."""
        if self.tipe != "berkas":
            return

        acquired = self._acquire_file_lock()
        if not acquired:
            return

        try:
            # 🎯 Cek data. Hapus kunci metadata yang diawali underscore, kecuali 'sesi_id'
            data_user_saja = {
                k: v
                for k, v in self.data.items()
                if not k.startswith("_") or k == "sesi_id"
            }

            # Hanya simpan jika ada data pengguna selain metadata default ('sesi_id' pasti ada)
            if len(data_user_saja) <= 1:
                # Jika tidak ada data pengguna, hapus file lama (jika ada)
                if self.file_path.exists():
                    try:
                        self.file_path.unlink()
                    except Exception as e:
                        print(f"[tarri | sesi] Gagal menghapus sesi kosong: {e}")
                return

            # 🆕 Atomic write: tulis ke file temporary dulu, lalu rename
            try:
                temp_file = self.file_path.with_suffix(".tmp")

                safe_data = {}
                for k, v in self.data.items():
                    try:
                        json.dumps(v)
                        safe_data[k] = v
                    except TypeError:
                        safe_data[k] = {"value": str(v), "created": time.time()}

                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(safe_data, f, indent=2, ensure_ascii=False)

                # 🆕 Atomic replace
                temp_file.replace(self.file_path)

            except Exception as e:
                print(f"[tarri | sesi] Gagal menyimpan sesi {self.sesi_id[:10]}: {e}")
        finally:
            self._release_file_lock()

    # 🆕 Alias untuk compatibility dengan kode lama
    def _muat(self):
        return self._muat_dengan_lock()

    def _simpan(self):
        return self._simpan_dengan_lock()

    # ==============================
    # AKSI SESI DENGAN LOCKING
    # ==============================
    def hancurkan(self) -> bool:
        """Hancurkan session dengan locking"""
        with self._lock:
            try:
                # Hapus file fisik
                if self.file_path.exists():
                    os.remove(self.file_path)

                # Hapus lock file
                if self.lock_file.exists():
                    self.lock_file.unlink()

                # Kosongkan data di memori objek ini
                self.data = {}

                # 🆕 Reset global instance jika ini adalah instance global
                global _GLOBAL_SESI
                with _MODULE_LOCK:
                    if _GLOBAL_SESI is self:
                        _GLOBAL_SESI = None

                return True
            except Exception as e:
                print(f"[tarri | sesi] Gagal total menghancurkan sesi: {e}")
                return False

    def ambil(self, key, default=None):
        """Ambil data dari session dengan locking"""
        with self._lock:
            self._muat_dengan_lock()
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
        """Ambil semua data session dengan locking"""
        with self._lock:
            self._muat_dengan_lock()
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
        Dengan locking.
        """
        with self._lock:
            self._muat_dengan_lock()
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
                self._simpan_dengan_lock()
                return True

            # 4. Gagal (tidak ada yang ditemukan/dihapus)
            return False

    def perbarui(self, data):
        """Update session data dengan locking"""
        with self._lock:
            self._muat_dengan_lock()
            now = time.time()
            if isinstance(data, dict):
                cleaned = {}
                for k, v in data.items():
                    key = self._unwrap(k)
                    val = self._unwrap(v)
                    cleaned[key] = {"value": val, "created": now}
                self.data.update(cleaned)
                self._simpan_dengan_lock()
                return {k: v["value"] for k, v in cleaned.items()}
            else:
                self.data = {"value": self._unwrap(data), "created": now}
                self._simpan_dengan_lock()
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
def buat_sesi(
    browser_sesi_id: Optional[str] = None, lokasi: Optional[str] = None
) -> SesiManager:
    """Buat instance SesiManager baru untuk tiap browser/client"""
    return SesiManager(lokasi=lokasi, sesi_id=browser_sesi_id)


# =========================
# API GLOBAL (Perbaikan dengan Lazy Initialization dan Locking)
# =========================


def sesi_hancurkan():
    """API Global untuk menghancurkan sesi yang sedang aktif."""
    with _MODULE_LOCK:
        _sesi = _get_global_sesi()
        return _sesi.hancurkan()


def _get_global_sesi() -> SesiManager:
    """Menginisialisasi sesi global (untuk API) hanya saat diakses."""
    global _GLOBAL_SESI
    with _MODULE_LOCK:
        if _GLOBAL_SESI is None:
            # Inisialisasi sesi fallback dengan locking
            _GLOBAL_SESI = SesiManager()
        return _GLOBAL_SESI


# 🆕 Semua fungsi API menggunakan module lock
def sesi_simpan(*args, **kwargs):
    """Simpan data ke session dengan locking"""
    with _MODULE_LOCK:
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
    """Ambil data dari session dengan locking"""
    with _MODULE_LOCK:
        _sesi = _get_global_sesi()

        # 🆕 Verifikasi session file masih ada
        if _sesi.tipe == "berkas" and hasattr(_sesi, "file_path"):
            if _sesi.file_path.exists():
                # Cek expiration
                try:
                    mtime = _sesi.file_path.stat().st_mtime
                    if time.time() - mtime > _sesi.EXPIRE_SECS:
                        # Session expired
                        _sesi.data = {}
                except:
                    pass
            else:
                # File tidak ada, reset data
                _sesi.data = {}

        if not args:
            return _sesi.semua()

        hasil = {k: _sesi.ambil(k, default) for k in args}
        return list(hasil.values())[0] if len(args) == 1 else hasil


def sesi_hapus(k: Union[str, List[str]]):
    """
    Menghapus kunci sesi dengan locking.
    Menerima string tunggal atau list/array string.
    """
    with _MODULE_LOCK:
        _sesi = _get_global_sesi()
        return _sesi.hapus(k)


def sesi_semua():
    """Ambil semua data session dengan locking"""
    with _MODULE_LOCK:
        _sesi = _get_global_sesi()
        return _sesi.semua()


def sesi_perbarui(data):
    """Update session data dengan locking"""
    with _MODULE_LOCK:
        _sesi = _get_global_sesi()
        return _sesi.perbarui(data)


def sesi_tipe(self, tipe=None):
    """Set atau get session type dengan locking"""
    # Asumsi self.session diatur oleh interpreter Tarri
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    with self.session._lock:
        if tipe:
            self.session.tipe = tipe
        return self.session.tipe


def sesi_lokasi(self, lokasi=None):
    """Set atau get session location dengan locking"""
    # Asumsi self.session diatur oleh interpreter Tarri
    if not hasattr(self, "session"):
        print("[tarri | sesi] Interpreter belum punya session")
        return None
    with self.session._lock:
        if lokasi:
            self.session.lokasi = Path(lokasi)
            os.makedirs(self.session.lokasi, exist_ok=True)
        return str(self.session.lokasi)


# =========================
# API GLOBAL (lanjutan)
# =========================

# Tambahkan alias sesi agar modul lain bisa mengimpornya
sesi = _get_global_sesi()
