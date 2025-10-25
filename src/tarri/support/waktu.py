import datetime
import calendar
import datetime

def jam():
    """
    Menampilkan jam saat ini (HH:MM:SS).
    """
    sekarang = datetime.datetime.now()
    return sekarang.strftime("%H:%M:%S")

def tanggal():
    """
    Menampilkan tanggal hari ini (YYYY-MM-DD).
    """
    sekarang = datetime.datetime.now()
    return sekarang.strftime("%Y-%m-%d")

def kalender(bulan=None, tahun=None):
    """
    Menampilkan kalender bulan/tahun tertentu.
    Jika tidak ada argumen, pakai bulan & tahun sekarang.
    """
    now = datetime.datetime.now()
    bulan = bulan or now.month
    tahun = tahun or now.year

    return calendar.month(tahun, bulan)
