import math
from decimal import Decimal, getcontext


# -----------------------------
# 🔢 Fungsi Cek Bilangan
# -----------------------------

def bilangan_prima(n):
    """Mengembalikan bilangan prima dari n. Bisa tunggal atau list."""
    def _cek(x):
        if x < 2 or x != int(x):
            return False
        for i in range(2, int(math.sqrt(x)) + 1):
            if x % i == 0:
                return False
        return True

    if isinstance(n, list):
        return [int(x) for x in n if _cek(x)]
    return [int(n)] if _cek(n) else []


def bilangan_ganjil(n):
    """Mengembalikan bilangan ganjil dari n. Bisa tunggal atau list."""
    def _cek(x):
        return x % 2 != 0 if x == int(x) else False

    if isinstance(n, list):
        return [int(x) for x in n if _cek(x)]
    return [int(n)] if _cek(n) else []


def bilangan_genap(n):
    """Mengembalikan bilangan genap dari n. Bisa tunggal atau list."""
    def _cek(x):
        return x % 2 == 0 if x == int(x) else False

    if isinstance(n, list):
        return [int(x) for x in n if _cek(x)]
    return [int(n)] if _cek(n) else []


def bilangan_negatif(n):
    """Mengembalikan bilangan negatif dari n. Bisa tunggal atau list. Bulat tetap int."""
    def _cek(x):
        return x < 0

    def _format(x):
        return int(x) if x == int(x) else x

    if isinstance(n, list):
        return [_format(x) for x in n if _cek(x)]
    return [_format(n)] if _cek(n) else []


def bilangan_pecahan(n):
    """Mengembalikan bilangan pecahan/desimal dari n. Bisa tunggal atau list."""
    def _cek(x):
        return x != int(x)

    if isinstance(n, list):
        return [x for x in n if _cek(x)]
    return [n] if _cek(n) else []

def bilangan_fibonacci(n):
    """
    Cetak deret Fibonacci sebanyak n angka pertama, tanpa tanda []
    """
    if n <= 0:
        return []
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def pi(*args):
    """
    Mengembalikan π dengan presisi sesuai jumlah digit.
    Default 2 digit jika tidak ada argumen.
    """
    # Cek args kosong
    if not args or args[0] is None:
        digits = 2
    else:
        digits = int(args[0])

    getcontext().prec = digits + 2
    pi_val = Decimal("3.14159265358979323846264338327950288419716939937510")
    return f"{pi_val:.{digits}f}"

# -----------------------------
# 🔢 Fungsi Cek Semua Kategori Sekaligus
# -----------------------------
def cek_bilangan(n):
    """
    Mengembalikan string rapi dari kategori bilangan:
    ganjil, genap, prima, negatif, pecahan.
    Hanya angka unik, bulat -> int, pecahan -> float
    """
    def uniq(lst):
        seen = set()
        result = []
        for x in lst:
            val = int(x) if x == int(x) else x
            if val not in seen:
                seen.add(val)
                result.append(val)
        return result

    categories = {
        "ganjil": uniq(bilangan_ganjil(n)),
        "genap": uniq(bilangan_genap(n)),
        "prima": uniq(bilangan_prima(n)),
        "negatif": uniq(bilangan_negatif(n)),
        "pecahan": uniq(bilangan_pecahan(n))
    }

    # ubah menjadi string tanpa {}, '', urutannya tetap
    output = []
    for k, v in categories.items():
        output.append(f"{k}: {', '.join(str(x) for x in v)}")
    return "\n".join(output)
