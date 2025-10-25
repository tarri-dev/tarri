import random
import math
import statistics


# Utilitas bantu
def _bersihkan(x):
    """Konversi float ke int bila nilainya bilangan bulat."""
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x


# 🔢 Dasar
def acak(min_val: int, max_val: int):
    """Menghasilkan angka acak antara min_val dan max_val (inklusif)."""
    return random.randint(min_val, max_val)


def akar(x: float):
    """Menghitung akar kuadrat dari x."""
    return _bersihkan(math.sqrt(x))


def pangkat(a: float, b: float):
    """Menghitung a pangkat b."""
    return _bersihkan(math.pow(a, b))


def bulatkan(x: float, n: int = 0):
    """Membulatkan angka x ke n digit desimal."""
    return _bersihkan(round(x, n))


def maksimal(daftar: list):
    """Mengembalikan nilai maksimum dari daftar angka."""
    return _bersihkan(max(daftar))


def minimal(daftar: list):
    """Mengembalikan nilai minimum dari daftar angka."""
    return _bersihkan(min(daftar))


def rata_rata(daftar: list):
    """Menghitung rata-rata dari daftar angka."""
    if not daftar:
        return 0
    return _bersihkan(sum(daftar) / len(daftar))


def faktorial(n: int):
    """Menghitung faktorial dari n."""
    return math.factorial(n)


def mod(a: int, b: int):
    """Menghitung sisa hasil bagi a dibagi b."""
    return a % b


# 📐 Trigonometri
def sin(x: float):
    """Menghitung sinus dari x (radian)."""
    return _bersihkan(math.sin(x))


def cos(x: float):
    """Menghitung cosinus dari x (radian)."""
    return _bersihkan(math.cos(x))


def tan(x: float):
    """Menghitung tangen dari x (radian)."""
    return _bersihkan(math.tan(x))


def derajat(x: float):
    """Konversi radian ke derajat."""
    return _bersihkan(math.degrees(x))


def radian(x: float):
    """Konversi derajat ke radian."""
    return _bersihkan(math.radians(x))


# 📊 Statistik
def median(daftar: list):
    """Menghitung median dari daftar angka."""
    return _bersihkan(statistics.median(daftar))


def variansi(daftar: list):
    """Menghitung variansi dari daftar angka."""
    if len(daftar) <= 1:
        return 0
    return _bersihkan(statistics.variance(daftar))


def std_dev(daftar: list):
    """Menghitung standar deviasi dari daftar angka."""
    if len(daftar) <= 1:
        return 0
    return _bersihkan(statistics.stdev(daftar))


# 🔮 Lainnya
def log(x: float, base: float = math.e):
    """Menghitung logaritma dari x dengan basis tertentu."""
    return _bersihkan(math.log(x, base))


def exp(x: float):
    """Menghitung eksponensial e^x."""
    return _bersihkan(math.exp(x))


def floor(x: float):
    """Membulatkan x ke bawah (bilangan bulat terdekat)."""
    return math.floor(x)


def ceil(x: float):
    """Membulatkan x ke atas (bilangan bulat terdekat)."""
    return math.ceil(x)
