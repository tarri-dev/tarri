import random
import math
import statistics


def acak(min_val: int, max_val: int) -> int:
    """
    Menghasilkan angka acak antara min_val dan max_val (inklusif).
    """
    return random.randint(min_val, max_val)


def akar(x: float) -> float:
    """
    Menghitung akar kuadrat dari x.
    """
    return math.sqrt(x)


def pangkat(a: float, b: float) -> float:
    """
    Menghitung a pangkat b.
    """
    return math.pow(a, b)


def bulatkan(x: float, n: int = 0) -> float:
    """
    Membulatkan angka x ke n digit desimal.
    Default: n=0 (membulatkan ke bilangan bulat).
    """
    return round(x, n)


def maksimal(daftar: list) -> float:
    """
    Mengembalikan nilai maksimum dari daftar angka.
    """
    return max(daftar)


def minimal(daftar: list) -> float:
    """
    Mengembalikan nilai minimum dari daftar angka.
    """
    return min(daftar)


def rata_rata(daftar: list) -> float:
    """
    Menghitung rata-rata dari daftar angka.
    """
    return sum(daftar) / len(daftar) if daftar else 0


# 🔢 Dasar tambahan
def faktorial(n: int) -> int:
    """
    Menghitung faktorial dari n.
    """
    return math.factorial(n)


def mod(a: int, b: int) -> int:
    """
    Menghitung sisa hasil bagi a dibagi b.
    """
    return a % b


# 📐 Trigonometri
def sin(x: float) -> float:
    """
    Menghitung sinus dari x (radian).
    """
    return math.sin(x)


def cos(x: float) -> float:
    """
    Menghitung cosinus dari x (radian).
    """
    return math.cos(x)


def tan(x: float) -> float:
    """
    Menghitung tangen dari x (radian).
    """
    return math.tan(x)


def derajat(x: float) -> float:
    """
    Konversi radian ke derajat.
    """
    return math.degrees(x)


def radian(x: float) -> float:
    """
    Konversi derajat ke radian.
    """
    return math.radians(x)


# 📊 Statistik
def jumlah(daftar: list) -> float:
    """
    Menjumlahkan semua elemen dalam daftar angka.
    """
    return sum(daftar)


def median(daftar: list) -> float:
    """
    Menghitung median dari daftar angka.
    """
    return statistics.median(daftar)


def variansi(daftar: list) -> float:
    """
    Menghitung variansi dari daftar angka.
    """
    return statistics.variance(daftar) if len(daftar) > 1 else 0


def std_dev(daftar: list) -> float:
    """
    Menghitung standar deviasi dari daftar angka.
    """
    return statistics.stdev(daftar) if len(daftar) > 1 else 0


# 🔮 Lainnya
def log(x: float, base: float = math.e) -> float:
    """
    Menghitung logaritma dari x dengan basis tertentu.
    Default basis = e.
    """
    return math.log(x, base)


def exp(x: float) -> float:
    """
    Menghitung eksponensial e^x.
    """
    return math.exp(x)


def floor(x: float) -> int:
    """
    Membulatkan x ke bawah (bilangan bulat terdekat).
    """
    return math.floor(x)


def ceil(x: float) -> int:
    """
    Membulatkan x ke atas (bilangan bulat terdekat).
    """
    return math.ceil(x)


