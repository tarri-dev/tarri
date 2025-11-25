# =====================================================
# call_function.py - Handler fungsi built-in TARRI
# =====================================================

from tarri.functions.huruf_acak import huruf_acak
from tarri.functions.huruf_acak_rapi import huruf_acak_rapi
from tarri.functions.lorem_ipsum import lorem_ipsum
from tarri.functions.angka_acak import angka_acak
from tarri.functions.uuid import UUID
from tarri.functions.slug import slug
from tarri.functions.tipe_data import tipe_data
from tarri.functions.masukkan import masukkan
from tarri.functions.urutkan_data import urutkan_data
from tarri.functions.cari_data import cari_data
from tarri.functions.termasuk import termasuk
from tarri.functions.halaman import halaman
from tarri.functions.alihkan import alihkan
from tarri.functions.tujuan import tujuan
from tarri.functions.rute import rute
from tarri.functions.cetak import cetak
from tarri.functions.ctk import ctk
from tarri.functions.cetak_web import cetak_web
from tarri.functions.cetak_html import cetak_html
from tarri.functions.ctkw import ctkw
from tarri.functions.ctkh import ctkh
from tarri.functions.batalkan import batalkan
from tarri.functions.ubah_kata import ubah_kata
from tarri.functions.kembalikan_html import kembalikan_html
from tarri.functions.cetak_detail import cetak_detail
from tarri.functions.lacak import lacak
from tarri.functions.lempar_pesan import lempar_pesan
from tarri.functions.kata_bijak import kata_bijak
from tarri.functions.sandi import buat_sandi, cek_sandi
from tarri.functions.kelolaTxt import simpanTxt, bacaTxt, perbaruiTxt, hapusTxt
from tarri.functions.kelolaJson import baca_json, buat_json, simpan_json

# sqlite db
from tarri.db.sqlite import sqlite, tabel_sqlite

# mysql db
from tarri.db.mysql import mysql, tabel_mysql

from lark import Tree, Token


# support
from tarri.support import waktu,teks,matematika,waktu_proses,list,bilangan,lainya

# sesi
from tarri.session.sesi import sesi as sesi_py

def call_function(self, func_name, args):

    if isinstance(func_name, bool):
        return func_name

    if isinstance(func_name, str):
        name = func_name.lower()
    else:
        name = str(func_name).lower()

    if name in ["benar", "salah"]:
        return True if name == "benar" else False

    elif name == "null":
        return None

    # =====================================================
    # SQLite Database Integration
    # =====================================================
    elif func_name == "sqlite":
        try:
            # print(f"[DEBUG sqlite] func_name={func_name}, args={args}")
            aksi = args[0]
            argumen = args[1:]

            mapping = {
                "koneksi": sqlite.__koneksi__,
                "buat": sqlite.__buat__,
                "simpan": sqlite.__simpan__,
                "ubah": sqlite.__ubah__,
                "ambil": sqlite.__ambil__,
                "semua": sqlite.__semua__,
                "pertama": sqlite.__pertama__,
                "rapi": sqlite.__rapi__,
                "tabel": sqlite.__tabel__,
                "hapus": sqlite.__hapus__,
                "dimana": sqlite.__dimana__,
                "danDimana": sqlite.__danDimana__,
                "atauDimana": sqlite.__atauDimana__,
                "urutkan": sqlite.__urutkan__,
                
            }

            if aksi not in mapping:
                raise Exception(f"Aksi sqlite '{aksi}' tidak dikenal")

            return mapping[aksi](*argumen)
        except Exception as e:
            return f"Salah: {e}"
        
    # =====================================================
    # MySQL Database Integration
    # =====================================================
    elif func_name == "mysql":
        try:
            aksi = args[0]
            argumen = args[1:]

            mapping = {
                "koneksi": mysql.__koneksi__,
                "buat": mysql.__buat__,
                "simpan": mysql.__simpan__,
                "ubah": mysql.__ubah__,
                "ambil": mysql.__ambil__,
                "semua": mysql.__semua__,
                "pertama": mysql.__pertama__,
                "rapi": mysql.__rapi__,
                "tabel": mysql.__tabel__,
                "hapus": mysql.__hapus__,
                "dimana": mysql.__dimana__,
                "danDimana": mysql.__danDimana__,
                "atauDimana": mysql.__atauDimana__,
                "urutkan": mysql.__urutkan__,
            }

            if aksi not in mapping:
                raise Exception(f"Aksi mysql '{aksi}' tidak dikenal")

            return mapping[aksi](*argumen)
        except Exception as e:
            return f"Salah: {e}"


    elif func_name == "tabel_sqlite":
        try:
            return tabel_sqlite()
        except Exception as e:
            return f"Salah: {e}"
        
    elif func_name == "tabel_mysql":
        try:
            return tabel_mysql()
        except Exception as e:
            return f"Salah: {e}"


    # =====================================================
    # Fungsi Input / Utility
    # =====================================================
    if func_name == "masukkan":
        return masukkan(self, args)
    
    elif func_name == "batalkan":
        return batalkan(*args)

    elif func_name == "cari_data":
        return cari_data(self, args)
    
    elif func_name == "urutkan_data":
        return urutkan_data(self, args)
    
    elif func_name == "termasuk":
        return termasuk(self, args)
    
    elif func_name == "rute":
        return rute(self, args)
    
    elif func_name == "tujuan":
        return tujuan(args)
    
    elif func_name == "halaman":
        return halaman(self, args)
    
    elif func_name == "alihkan":
        return alihkan(self, args)
    
    elif func_name in ["cetak", "ctk"]:
        args_eval = []
        for a in args:
            if isinstance(a, Tree) and a.data == "call_expr":
                args_eval.append(self.evaluate_expr(a))
            else:
                args_eval.append(self.eval_arg(a))

        konteks = getattr(self, "context", {}).copy()

        if func_name == "cetak":
            return cetak(*args_eval, konteks=konteks)
        else:
            return ctk(*args_eval, konteks=konteks)


    elif func_name == "cetak_web":
        return cetak_web(self, args)
    
    elif func_name == "ctkw":
        return ctkw(self, args)

    elif func_name == "cetak_html":
        return cetak_html(self, args)
    
    elif func_name == "ctkh":
        return ctkh(self, args)
    
    elif func_name == "cetak_detail":
        return cetak_detail(args)
    
    elif func_name == "kembalikan_html":
        return kembalikan_html(args, self)

    elif func_name == "lacak":
        return lacak(self, args)
    
    elif func_name == "lempar_pesan":
        return lempar_pesan(args)


    # =====================================================
    # Fungsi Sesi Lanjutan (file/memori) – per-browser
    # =====================================================
    elif func_name == "sesi":
        return sesi_py(self, args)

    elif func_name == "sesi_tipe":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        return self.session.tipe if not args else self.session.set_tipe(args[0])

    elif func_name == "sesi_lokasi":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        return str(self.session.lokasi)

    elif func_name == "sesi_simpan":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")

        # Jika argumen 1 berupa dict → langsung perbarui
        if len(args) == 1 and isinstance(args[0], dict):
            return self.session.perbarui(args[0])

        # Jika pasangan key/value → harus genap minimal 2
        if len(args) < 2 or len(args) % 2 != 0:
            self.error("[tarri | sesi] Minimal pasangan dua argumen atau dictionary")
            return None

    elif func_name == "sesi_ambil":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        if not args:
            return self.session.semua()
        elif len(args) == 1:
            return self.session.ambil(args[0])
        else:
            return {k: self.session.ambil(k) for k in args}

    elif func_name == "sesi_semua":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        return self.session.semua()

    elif func_name == "sesi_hapus":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        if not args:
            self.error("[tarri | sesi] Hapus membutuhkan satu argumen")
            return None
        return self.session.hapus(args[0])

    elif func_name == "sesi_perbarui":
        if not hasattr(self, "session"):
            self.error("[tarri | sesi] Interpreter belum punya sesi")
        if not args:
            self.error("[tarri | sesi] Perbarui membutuhkan minimal satu argumen")
            return None
        if isinstance(args[0], dict):
            return self.session.perbarui(args[0])
        self.error("[tarri | sesi] Argumen harus dictionary")
        return None



    # =====================================================
    # Fungsi Random / Utility
    # =====================================================
    elif func_name == "huruf_acak":
        return huruf_acak(args[0] if args else 5)
    
    elif func_name == "huruf_acak_rapi":
        return huruf_acak_rapi(args[0])
    
    elif func_name == "lorem_ipsum":
        return lorem_ipsum(args[0] if args else 5)
    elif func_name == "angka_acak":
        if len(args) == 2:
            return angka_acak(args[0], args[1])
        elif len(args) == 1:
            return angka_acak(0, args[0])
        return angka_acak()
    elif func_name == "UUID":
        return UUID()
    elif func_name == "slug":
        return slug(args[0])
    elif func_name == "tipe_data":
        return tipe_data(args[0])
    elif func_name == "buat_sandi":
        return buat_sandi(str(args[0]) if args else "")
    elif func_name == "cek_sandi":
        if len(args) < 2:
            self.error("cekSandi butuh 2 argumen: (password_plain, hash_salt)")
            return False
        return cek_sandi(args[0], args[1])

    # =====================================================
    # File / Text /JSON
    # =====================================================
    # TXT
    elif func_name == "simpanTxt":
        return simpanTxt(args[0], args[1], ctx=self.context, tarri_file=getattr(self, "current_file", None))
    elif func_name == "bacaTxt":
        key_arg = args[1] if len(args) > 1 else None
        return bacaTxt(args[0], key=key_arg, ctx=self.context, tarri_file=getattr(self, "current_file", None))
    elif func_name == "perbaruiTxt":
        if len(args) == 2:
            return perbaruiTxt(args[0], "ganti", args[1], ctx=self.context, tarri_file=getattr(self, "current_file", None))
        elif len(args) >= 3:
            return perbaruiTxt(args[0], args[1], args[2], ctx=self.context, tarri_file=getattr(self, "current_file", None))
    elif func_name == "hapusTxt":
        return hapusTxt(args[0], ctx=self.context, tarri_file=getattr(self, "current_file", None))
    
    # JSON
    elif func_name == "buat_json":
        return buat_json(args[0])

    elif func_name == "baca_json":
        return baca_json(args[0])
    
    elif func_name == "simpan_json":
        return simpan_json(args[0], args[1], args[2])

    # =====================================================
    # Support Functions (waktu, teks, matematika)
    # =====================================================
    elif func_name == "waktu_proses":
        return waktu_proses()
    elif func_name == "jam":
        return waktu.jam()
    elif func_name == "tanggal":
        return waktu.tanggal()
    elif func_name == "kalender":
        if len(args) == 2:
            return waktu.kalender(args[0], args[1])
        elif len(args) == 1:
            return waktu.kalender(args[0])
        return waktu.kalender()
    elif func_name == "panjang":
        return teks.panjang(args[0])
    elif func_name == "awal_kapital":
        return teks.awal_kapital(args[0])
    elif func_name == "ubah_kata":
        return ubah_kata(args[0])
    elif func_name == "kunci":
        return teks.kunci(args[0])
    elif func_name == "nilai":
        return teks.nilai(args[0])
    elif func_name == "besar":
        return teks.besar(args[0])
    elif func_name == "kecil":
        return teks.kecil(args[0])
    elif func_name == "ganti":
        return teks.ganti(args[0], args[1], args[2])
    elif func_name == "gabung":
        return teks.gabung(args[0], args[1] if len(args) > 1 else "")

    # =====================================================
    # Matematika
    # =====================================================
    elif func_name == "acak":
        return matematika.acak(args[0], args[1])
    elif func_name == "akar":
        return matematika.akar(args[0])
    elif func_name == "pangkat":
        return matematika.pangkat(args[0], args[1])
    elif func_name == "bulatkan":
        return matematika.bulatkan(args[0], args[1] if len(args) > 1 else 0)
    elif func_name == "maksimal":
        return matematika.maksimal(args[0])
    elif func_name == "minimal":
        return matematika.minimal(args[0])
    elif func_name == "rata_rata":
        return matematika.rata_rata(args[0])
    elif func_name == "faktorial":
        return matematika.faktorial(args[0])
    elif func_name == "mod":
        return matematika.mod(args[0], args[1])

    # =====================================================
    # Trigonometri
    # =====================================================
    elif func_name == "sin":
        return matematika.sin(args[0])
    elif func_name == "cos":
        return matematika.cos(args[0])
    elif func_name == "tan":
        return matematika.tan(args[0])
    elif func_name == "derajat":
        return matematika.derajat(args[0])
    elif func_name == "radian":
        return matematika.radian(args[0])

    # =====================================================
    # Statistik
    # =====================================================
    elif func_name == "median":
        return matematika.median(args[0])
    elif func_name == "variansi":
        return matematika.variansi(args[0])
    elif func_name == "std_dev":
        return matematika.std_dev(args[0])
    
    # =====================================================
    # List
    # =====================================================
    elif func_name == "unik":
        return list.unik(args[0])

    elif func_name == "cari_index":
        return list.cari_index(args[0], args[1])

    elif func_name == "hapus_index":
        return list.hapus_index(args[0], args[1])

    elif func_name == "balik":
        return list.balik(args[0])
    
    # =====================================================
    # Bilangan
    # =====================================================
    elif func_name == "bilangan_prima":
        return bilangan.bilangan_prima(args[0])

    elif func_name == "bilangan_ganjil":
        return bilangan.bilangan_ganjil(args[0])

    elif func_name == "bilangan_negatif":
        return bilangan.bilangan_negatif(args[0])

    elif func_name == "bilangan_pecahan":
        return bilangan.bilangan_pecahan(args[0])
    
    elif func_name == "bilangan_genap":
        return bilangan.bilangan_genap(args[0])
    
    elif func_name == "bilangan_fibonacci":
        return bilangan.bilangan_fibonacci(args[0])
    
    elif func_name == "cek_bilangan":
        return bilangan.cek_bilangan(args[0])
    
    elif func_name == "pi":
        digits = args[0] if args else 2
        return bilangan.pi(digits)

    
    
    # =====================================================
    # Lainnya
    # =====================================================
    elif func_name == "log":
        return matematika.log(args[0], args[1]) if len(args) > 1 else matematika.log(args[0])
    elif func_name == "exp":
        return matematika.exp(args[0])
    elif func_name == "floor":
        return matematika.floor(args[0])
    elif func_name == "ceil":
        return matematika.ceil(args[0])
    
    elif func_name == "kata_bijak":
        return kata_bijak()
    elif func_name == "jumlah":
        return lainya.jumlah(self, args)
    elif func_name == "ada":
        return lainya.ada(self, args)
    elif func_name == "semua":
        return lainya.semua(self, args)
    elif func_name == "himpunan":
        return lainya.himpunan(self, args)

    
    import builtins

    if isinstance(func_name, builtins.list):
        func_name = ".".join(str(x) for x in func_name if x)

    elif func_name in getattr(self, "functions", {}):
        return self.exec_func_call(func_name, args)

    elif func_name in ["cetak"]:
        self.error(f"Fungsi '{func_name}' dipanggil, tapi tidak berada di blok titikawal{{ ... }}!")
    else:
        self.error(f"Fungsi '{func_name}' tidak ditemukan")

    return None

