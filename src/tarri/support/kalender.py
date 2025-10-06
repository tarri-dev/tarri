import calendar
import datetime

def kalender(bulan=None, tahun=None):
    """
    Menampilkan kalender bulan/tahun tertentu.
    Jika tidak ada argumen, pakai bulan & tahun sekarang.
    """
    now = datetime.datetime.now()
    bulan = bulan or now.month
    tahun = tahun or now.year

    return calendar.month(tahun, bulan)
