# tarri/functions/rute.py
import re

ROUTES = []

class Rute:
    def __init__(self):
        self._last = None
        
    def __call__(self, url_path, target, method="GET", fungsi=None):
        """
        Supaya rute(...) bisa dipanggil langsung.
        Ini digunakan oleh loader rute.tarri.
        """
        regex, param_names = self._compile(url_path)
        ROUTES.append((method.upper(), regex, target.strip(), fungsi, param_names))
        return ""

    def post(self, url_path, target):
        regex, param_names = self._compile(url_path)
        self._last = ("POST", regex, target.strip(), None, param_names)
        ROUTES.append(self._last)
        return self  # biar bisa chaining `untuk fungsi(...)`

    def get(self, url_path, target):
        regex, param_names = self._compile(url_path)
        self._last = ("GET", regex, target.strip(), None, param_names)
        ROUTES.append(self._last)
        return self

    def fungsi(self, nama):
        if self._last:
            method, regex, target, _, param_names = self._last
            self._last = (method, regex, target, nama.strip(), param_names)
            ROUTES[-1] = self._last
        return self

    def _compile(self, url_path):
        """
        Compile URL path dengan {parameter} menjadi regex,
        dan ambil nama parameter-nya.
        """
        param_names = re.findall(r"\{([^\}]+)\}", url_path)
        pattern = re.sub(r"\{[^\}]+\}", r"([^/]+)", url_path.strip())
        regex = re.compile(f"^{pattern}$")
        return regex, param_names

# Instance tunggal
rute = Rute()
