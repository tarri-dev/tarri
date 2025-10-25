import os
import sys
import datetime
import threading
import getpass
import platform
from contextlib import contextmanager
from tarri import __version__  # versi Tarri

# -------------------------
# Logger Tarri
# -------------------------
class TarriLogger:
    """Logger Tarri lengkap, otomatis, dan thread-safe."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        # Folder log
        self.log_dir = os.path.expanduser("~/.tarri/logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # File log
        self.log_file = os.path.join(
            self.log_dir, datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        )
        self._lock = threading.Lock()

        if not os.path.exists(self.log_file):
            self._write_file("INFO", "=== LOG BARU DIMULAI ===")
            self._write_file("INFO", f"Versi Tarri: {__version__}")
            self._write_file("INFO", f"Pengguna   : {getpass.getuser()}")
            self._write_file("INFO", f"Perangkat  : {platform.node()}")
            self._write_file("INFO", f"OS         : {platform.system()} {platform.release()}")
            self._write_file("INFO", f"Python     : {platform.python_version()}")
            self._write_file("INFO", f"Waktu      : {datetime.datetime.now()}")

    def _timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def _write_file(self, level, message):
        line = f"[{self._timestamp()}] [{level}] {message}\n"
        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)

    # --------- API standar ---------
    def info(self, message):  self._write_file("INFO", message)
    def warn(self, message):  self._write_file("WARN", message)
    def error(self, message): self._write_file("ERROR", message)
    def debug(self, message): self._write_file("DEBUG", message)
    def garis(self): self._write_file("----", "-"*40)

    def show_log_path(self):
        print(f"[tarri | log] Menulis ke: {self.log_file}")

# Singleton global
logger = TarriLogger()

# -------------------------
# Redirect stdout/stderr ke log
# -------------------------
class TarriStreamRedirector:
    def __init__(self, stream, level="INFO"):
        self.stream = stream
        self.level = level

    def write(self, message):
        if message.strip():  # skip empty lines
            logger._write_file(self.level, message)
        self.stream.write(message)
        self.stream.flush()

    def flush(self):
        self.stream.flush()

@contextmanager
def redirect_stdout_stderr(level_stdout="INFO", level_stderr="ERROR"):
    """Redirect sementara stdout/stderr ke logger"""
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = TarriStreamRedirector(original_stdout, level_stdout)
    sys.stderr = TarriStreamRedirector(original_stderr, level_stderr)
    try:
        yield
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

# -------------------------
# Fungsi cetak() otomatis log
# -------------------------
def cetak(value):
    """Cetak ke layar dan log"""
    print(value)
    logger.info(f"CETAK: {value}")

# -------------------------
# Fungsi utilitas log
# -------------------------
def baca_log_terakhir(n=50):
    """Baca log terakhir n baris"""
    if not os.path.exists(logger.log_file):
        print("[tarri | log] Tidak ada log ditemukan.")
        return
    with open(logger.log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    tail = lines[-n:] if len(lines) > n else lines
    for line in tail:
        print(line.strip())

def hapus_semua_log():
    """Hapus semua log dengan konfirmasi"""
    confirm = input("Hapus semua log?  ya | tidak : ").strip().lower()
    if confirm != "ya":
        print("[tarri | log] Batal menghapus log.")
        return
    for file in os.listdir(logger.log_dir):
        path = os.path.join(logger.log_dir, file)
        if os.path.isfile(path):
            os.remove(path)
    print("[tarri | log] Semua log telah dihapus.")


