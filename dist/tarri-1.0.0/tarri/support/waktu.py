#==============================================================================#
# File    : waktu.py                                                           #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Fungsi dan utilitas pendukung 'waktu' yang membantu operasi inti           #
#   Tarri.                                                                     #
#==============================================================================#

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
