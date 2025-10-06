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
