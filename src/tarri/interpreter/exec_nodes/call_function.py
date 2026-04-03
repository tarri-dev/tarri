# === IMPORTS ===

# Fungsi built-in
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

import tarri.functions.halaman
import tarri.functions.alihkan

from tarri.functions.tujuan import tujuan
from tarri.functions.rute import rute
from tarri.functions.cetak import cetak
from tarri.functions.ctk import ctk
from tarri.functions.cetak_web import cetak_web
from tarri.functions.cetak_html import cetak_html
from tarri.functions.ctkw import ctkw
from tarri.functions.ctkh import ctkh
from tarri.functions.batalkan import batalkan
from tarri.functions.tukar import tukar
from tarri.functions.ubah_kata import ubah_kata
from tarri.functions.kembalikan_html import kembalikan_html
from tarri.functions.cetak_detail import cetak_detail
from tarri.functions.lacak import lacak
from tarri.functions.lempar_pesan import lempar_pesan
from tarri.functions.kata_bijak import kata_bijak
from tarri.functions.json import json
from tarri.functions.sandi import buat_sandi, cek_sandi
from tarri.functions.kelolaTxt import simpanTxt, bacaTxt, perbaruiTxt, hapusTxt
from tarri.functions.kelolaJson import baca_json, buat_json, simpan_json

# API
from tarri.kelola_api.ambil_data_api import ambil_data_api
from tarri.kelola_api.simpan_data_api import simpan_data_api
from tarri.kelola_api.parse_json_api import parse_json_api
from tarri.kelola_api.cek_data_api import cek_data_api
from tarri.kelola_api.cari_data_api import cari_data_api
from tarri.kelola_api.perbarui_data_api import perbarui_data_api
from tarri.kelola_api.hapus_data_api import hapus_data_api
from tarri.kelola_api.kirim_data_api import kirim_data_api

# Database
from tarri.db.sqlite import sqlite, tabel_sqlite
from tarri.db.mysql import mysql, tabel_mysql

from lark import Tree, Token
import builtins

# Support
from tarri.support import waktu, teks, matematika, waktu_proses, list, bilangan, lainya
from tarri.support.teks import subkata
from tarri.support.list import tambah

# Sesi
from tarri.session.sesi import sesi as sesi_py

# =====================================================
# DISPATCH TABLE — Daftar semua fungsi built-in
# =====================================================
#
# Format: "nama_fungsi": handler_function
# Handler menerima (ctx, args) dan mengembalikan nilai
#
# Untuk menambah fungsi baru, cukup tambahkan entry
# di kategori yang sesuai. Tidak perlu sentuh call_function().
#
# =====================================================

BUILTINS = {}


def daftar(*names):
    """Decorator untuk mendaftarkan fungsi built-in ke registry.

    Contoh penggunaan:
        @daftar("cetak", "ctk")
        def handle_cetak(ctx, args):
            ...
    """

    def wrapper(func):
        for name in names:
            BUILTINS[name] = func
        return func

    return wrapper


# =====================================================
# 1. CETAK / OUTPUT
# =====================================================


@daftar("cetak", "ctk")
def _handle_cetak(ctx, args):
    args_eval = []
    for a in args:
        if isinstance(a, Tree) and a.data == "call_expr":
            args_eval.append(ctx.evaluate_expr(a))
        else:
            args_eval.append(ctx.eval_arg(a))
    konteks = getattr(ctx, "context", {}).copy()
    if args[0] if args else None:  # disambiguate cetak vs ctk
        # Perlu cek nama asli — keduanya berbagi handler
        pass
    return cetak(*args_eval, konteks=konteks)


# Override khusus ctk (handler terpisah karena memanggil fungsi berbeda)
def _handle_ctk(ctx, args):
    args_eval = []
    for a in args:
        if isinstance(a, Tree) and a.data == "call_expr":
            args_eval.append(ctx.evaluate_expr(a))
        else:
            args_eval.append(ctx.eval_arg(a))
    konteks = getattr(ctx, "context", {}).copy()
    return ctk(*args_eval, konteks=konteks)


# Re-register ctk dengan handler spesifik
BUILTINS["ctk"] = _handle_ctk


@daftar("cetak_web")
def _handle_cetak_web(ctx, args):
    return cetak_web(ctx, args)


@daftar("ctkw")
def _handle_ctkw(ctx, args):
    return ctkw(ctx, args)


@daftar("cetak_html")
def _handle_cetak_html(ctx, args):
    return cetak_html(ctx, args)


@daftar("ctkh")
def _handle_ctkh(ctx, args):
    return ctkh(ctx, args)


@daftar("cetak_detail")
def _handle_cetak_detail(ctx, args):
    return cetak_detail(args)


@daftar("kembalikan_html")
def _handle_kembalikan_html(ctx, args):
    return kembalikan_html(args, ctx)


# =====================================================
# 2. INPUT / UTILITY
# =====================================================


@daftar("masukkan")
def _handle_masukkan(ctx, args):
    return masukkan(ctx, args)


@daftar("batalkan")
def _handle_batalkan(ctx, args):
    return batalkan(*args)


@daftar("json")
def _handle_json(ctx, args):
    return json(
        status=args[0] if len(args) > 0 else 200,
        message=args[1] if len(args) > 1 else "Sukses",
        data=args[2] if len(args) > 2 else None,
        meta=args[3] if len(args) > 3 else None,
        errors=args[4] if len(args) > 4 else None,
    )


@daftar("lacak")
def _handle_lacak(ctx, args):
    return lacak(ctx, args)


@daftar("lempar_pesan")
def _handle_lempar_pesan(ctx, args):
    return lempar_pesan(args)


# =====================================================
# 3. PENCARIAN & PENGURUTAN DATA
# =====================================================


@daftar("cari_data")
def _handle_cari_data(ctx, args):
    return cari_data(ctx, args)


@daftar("urutkan_data")
def _handle_urutkan_data(ctx, args):
    return urutkan_data(ctx, args)


@daftar("termasuk")
def _handle_termasuk(ctx, args):
    return termasuk(ctx, args)


# =====================================================
# 4. WEB / ROUTING
# =====================================================


@daftar("rute")
def _handle_rute(ctx, args):
    return rute(ctx, args)


@daftar("tujuan")
def _handle_tujuan(ctx, args):
    return tujuan(args)


@daftar("halaman")
def _handle_halaman(ctx, args):
    return tarri.functions.halaman.halaman(ctx, args)


@daftar("alihkan")
def _handle_alihkan(ctx, args):
    return tarri.functions.alihkan.alihkan(ctx, args)


@daftar("tukar")
def _handle_tukar(ctx, args):
    return tukar(args[0], args[1], args[2])


@daftar("ubah_kata")
def _handle_ubah_kata(ctx, args):
    return ubah_kata(args[0])


# =====================================================
# 5. DATABASE — SQLite
# =====================================================


@daftar("sqlite")
def _handle_sqlite(ctx, args):
    try:
        if not args:
            raise Exception(
                "Panggilan 'sqlite' membutuhkan aksi (misalnya, 'koneksi')."
            )
        aksi = args[0]
        argumen = args[1:]

        if aksi == "koneksi":
            if len(argumen) != 3:
                raise Exception(
                    "sqlite koneksi membutuhkan 3 argumen: lokasi, nama_db, nama_tabel."
                )
            return sqlite.koneksi(*argumen)

        raise Exception(
            f"Aksi sqlite global '{aksi}' tidak dikenal. Hanya 'koneksi' yang diizinkan."
        )
    except Exception as e:
        print(f"[tarri | sqlite | GAGAL] {e}")
        return None


@daftar("tabel_sqlite")
def _handle_tabel_sqlite(ctx, args):
    try:
        return tabel_sqlite()
    except Exception as e:
        return f"Salah: {e}"


# =====================================================
# 6. DATABASE — MySQL
# =====================================================


@daftar("mysql")
def _handle_mysql(ctx, args):
    try:
        if not args:
            raise Exception("Panggilan 'mysql' membutuhkan aksi (misalnya, 'koneksi').")
        aksi = args[0]
        argumen = args[1:]

        if aksi == "koneksi":
            if len(argumen) != 5:
                raise Exception(
                    "mysql koneksi membutuhkan 5 argumen: host, user, password, database, table."
                )
            return mysql.koneksi(*argumen)

        raise Exception(
            f"Aksi mysql global '{aksi}' tidak dikenal. Hanya 'koneksi' yang diizinkan."
        )
    except Exception as e:
        print(f"[tarri | mysql | GAGAL] {e}")
        return None


@daftar("tabel_mysql")
def _handle_tabel_mysql(ctx, args):
    try:
        return tabel_mysql()
    except Exception as e:
        return f"Salah: {e}"


# =====================================================
# 7. SESI (Session Management)
# =====================================================


@daftar("sesi")
def _handle_sesi(ctx, args):
    return sesi_py(ctx, args)


@daftar("sesi_hancurkan")
def _handle_sesi_hancurkan(ctx, args):
    if hasattr(ctx, "session"):
        return ctx.session.hancurkan()
    from tarri.session.sesi import sesi_hancurkan

    return sesi_hancurkan()


@daftar("sesi_tipe")
def _handle_sesi_tipe(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    return ctx.session.tipe if not args else ctx.session.set_tipe(args[0])


@daftar("sesi_lokasi")
def _handle_sesi_lokasi(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    return str(ctx.session.lokasi)


@daftar("sesi_simpan")
def _handle_sesi_simpan(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    # Kasus 1: Dictionary tunggal
    if len(args) == 1 and isinstance(args[0], dict):
        return ctx.session.perbarui(args[0])
    # Kasus 2: Pasangan key/value
    if len(args) >= 2 and len(args) % 2 == 0:
        data = {}
        for i in range(0, len(args), 2):
            data[args[i]] = args[i + 1]
        return ctx.session.perbarui(data)
    ctx.error(
        "[tarri | sesi] sesi_simpan membutuhkan (kamus_data) atau (kunci1, nilai1, kunci2, nilai2, ...)"
    )
    return None


@daftar("sesi_ambil")
def _handle_sesi_ambil(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    default_val = args[1] if len(args) > 1 else None
    if not args:
        return ctx.session.semua()
    elif len(args) == 1:
        return ctx.session.ambil(args[0])
    elif len(args) == 2 and not isinstance(args[0], builtins.list):
        return ctx.session.ambil(args[0], default_val)
    else:
        keys = args[0] if isinstance(args[0], builtins.list) else args
        return {k: ctx.session.ambil(k) for k in keys}


@daftar("sesi_semua")
def _handle_sesi_semua(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    return ctx.session.semua()


@daftar("sesi_hapus")
def _handle_sesi_hapus(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    if not args:
        ctx.error("[tarri | sesi] Hapus membutuhkan minimal satu argumen (kunci)")
        return None
    return ctx.session.hapus(args[0])


@daftar("sesi_perbarui")
def _handle_sesi_perbarui(ctx, args):
    if not hasattr(ctx, "session"):
        ctx.error("[tarri | sesi] Interpreter belum punya sesi")
        return None
    if not args or not isinstance(args[0], dict):
        ctx.error("[tarri | sesi] Perbarui membutuhkan argumen berupa kamus data (dictionary)")
        return None
    return ctx.session.perbarui(args[0])


# =====================================================
# 8. RANDOM / STRING UTILITY
# =====================================================


@daftar("huruf_acak")
def _handle_huruf_acak(ctx, args):
    return huruf_acak(args[0] if args else 5)


@daftar("huruf_acak_rapi")
def _handle_huruf_acak_rapi(ctx, args):
    return huruf_acak_rapi(args[0])


@daftar("lorem_ipsum")
def _handle_lorem_ipsum(ctx, args):
    return lorem_ipsum(args[0] if args else 5)


@daftar("angka_acak")
def _handle_angka_acak(ctx, args):
    if len(args) == 2:
        return angka_acak(args[0], args[1])
    elif len(args) == 1:
        return angka_acak(0, args[0])
    return angka_acak()


@daftar("UUID")
def _handle_uuid(ctx, args):
    return UUID()


@daftar("slug")
def _handle_slug(ctx, args):
    return slug(args[0])


@daftar("tipe_data")
def _handle_tipe_data(ctx, args):
    return tipe_data(args[0])


@daftar("buat_sandi")
def _handle_buat_sandi(ctx, args):
    return buat_sandi(str(args[0]) if args else "")


@daftar("cek_sandi")
def _handle_cek_sandi(ctx, args):
    if len(args) < 2:
        ctx.error("cek_sandi membutuhkan 2 argumen: (kata_sandi, hash_salt)")
        return False
    return cek_sandi(args[0], args[1])


@daftar("kata_bijak")
def _handle_kata_bijak(ctx, args):
    return kata_bijak()


# =====================================================
# 9. FILE — TXT
# =====================================================


@daftar("simpanTxt")
def _handle_simpan_txt(ctx, args):
    return simpanTxt(
        args[0], args[1], ctx=ctx.context, tarri_file=getattr(ctx, "current_file", None)
    )


@daftar("bacaTxt")
def _handle_baca_txt(ctx, args):
    key_arg = args[1] if len(args) > 1 else None
    return bacaTxt(
        args[0],
        key=key_arg,
        ctx=ctx.context,
        tarri_file=getattr(ctx, "current_file", None),
    )


@daftar("perbaruiTxt")
def _handle_perbarui_txt(ctx, args):
    if len(args) == 2:
        return perbaruiTxt(
            args[0],
            "ganti",
            args[1],
            ctx=ctx.context,
            tarri_file=getattr(ctx, "current_file", None),
        )
    elif len(args) >= 3:
        return perbaruiTxt(
            args[0],
            args[1],
            args[2],
            ctx=ctx.context,
            tarri_file=getattr(ctx, "current_file", None),
        )


@daftar("hapusTxt")
def _handle_hapus_txt(ctx, args):
    return hapusTxt(
        args[0], ctx=ctx.context, tarri_file=getattr(ctx, "current_file", None)
    )


# =====================================================
# 10. FILE — JSON
# =====================================================


@daftar("buat_json")
def _handle_buat_json(ctx, args):
    return buat_json(args[0])


@daftar("baca_json")
def _handle_baca_json(ctx, args):
    return baca_json(args[0])


@daftar("simpan_json")
def _handle_simpan_json(ctx, args):
    return simpan_json(args[0], args[1], args[2])


# =====================================================
# 11. WAKTU
# =====================================================


@daftar("waktu_proses")
def _handle_waktu_proses(ctx, args):
    return waktu_proses()


@daftar("jam")
def _handle_jam(ctx, args):
    return waktu.jam()


@daftar("tanggal")
def _handle_tanggal(ctx, args):
    return waktu.tanggal()


@daftar("kalender")
def _handle_kalender(ctx, args):
    if len(args) == 2:
        return waktu.kalender(args[0], args[1])
    elif len(args) == 1:
        return waktu.kalender(args[0])
    return waktu.kalender()


# =====================================================
# 12. TEKS
# =====================================================


@daftar("panjang")
def _handle_panjang(ctx, args):
    return teks.panjang(args[0])


@daftar("subkata")
def _handle_subkata(ctx, args):
    if len(args) < 2:
        ctx.error("Fungsi 'subkata' membutuhkan minimal 2 argumen: teks, mulai")
        return None
    teks_val = ctx.eval_arg(args[0])
    mulai_val = ctx.eval_arg(args[1])
    akhir_val = ctx.eval_arg(args[2]) if len(args) > 2 else None
    return subkata(teks_val, mulai_val, akhir_val)


@daftar("awal_kapital")
def _handle_awal_kapital(ctx, args):
    return teks.awal_kapital(args[0])


@daftar("ubah_kata")
def _handle_ubah_kata_fn(ctx, args):
    return ubah_kata(args[0])


@daftar("kunci")
def _handle_kunci(ctx, args):
    return teks.kunci(args[0])


@daftar("nilai")
def _handle_nilai(ctx, args):
    return teks.nilai(args[0])


@daftar("besar")
def _handle_besar(ctx, args):
    return teks.besar(args[0])


@daftar("kecil")
def _handle_kecil(ctx, args):
    return teks.kecil(args[0])


@daftar("ganti")
def _handle_ganti(ctx, args):
    return teks.ganti(args[0], args[1], args[2])


@daftar("gabung")
def _handle_gabung(ctx, args):
    return teks.gabung(args[0], args[1] if len(args) > 1 else "")


# =====================================================
# 13. MATEMATIKA
# =====================================================


@daftar("acak")
def _handle_acak(ctx, args):
    return matematika.acak(args[0], args[1])


@daftar("akar")
def _handle_akar(ctx, args):
    return matematika.akar(args[0])


@daftar("pangkat")
def _handle_pangkat(ctx, args):
    return matematika.pangkat(args[0], args[1])


@daftar("bulatkan")
def _handle_bulatkan(ctx, args):
    return matematika.bulatkan(args[0], args[1] if len(args) > 1 else 0)


@daftar("maksimal")
def _handle_maksimal(ctx, args):
    return matematika.maksimal(args[0])


@daftar("minimal")
def _handle_minimal(ctx, args):
    return matematika.minimal(args[0])


@daftar("rata_rata")
def _handle_rata_rata(ctx, args):
    return matematika.rata_rata(args[0])


@daftar("faktorial")
def _handle_faktorial(ctx, args):
    return matematika.faktorial(args[0])


@daftar("mod")
def _handle_mod(ctx, args):
    return matematika.mod(args[0], args[1])


# =====================================================
# 14. TRIGONOMETRI
# =====================================================


@daftar("sin")
def _handle_sin(ctx, args):
    return matematika.sin(args[0])


@daftar("cos")
def _handle_cos(ctx, args):
    return matematika.cos(args[0])


@daftar("tan")
def _handle_tan(ctx, args):
    return matematika.tan(args[0])


@daftar("derajat")
def _handle_derajat(ctx, args):
    return matematika.derajat(args[0])


@daftar("radian")
def _handle_radian(ctx, args):
    return matematika.radian(args[0])


# =====================================================
# 15. STATISTIK
# =====================================================


@daftar("median")
def _handle_median(ctx, args):
    return matematika.median(args[0])


@daftar("variansi")
def _handle_variansi(ctx, args):
    return matematika.variansi(args[0])


@daftar("std_dev")
def _handle_std_dev(ctx, args):
    return matematika.std_dev(args[0])


# =====================================================
# 16. LIST
# =====================================================


@daftar("unik")
def _handle_unik(ctx, args):
    return list.unik(args[0])


@daftar("tambah")
def _handle_tambah(ctx, args):
    if len(args) < 2:
        ctx.error("Fungsi 'tambah' membutuhkan 2 argumen: daftar, item")
        return None
    daftar_val = ctx.eval_arg(args[0])
    item_val = ctx.eval_arg(args[1])
    if not isinstance(daftar_val, builtins.list):
        ctx.error("Argumen pertama 'tambah' harus berupa daftar")
        return None
    return tambah(daftar_val, item_val)


@daftar("cari_index")
def _handle_cari_index(ctx, args):
    return list.cari_index(args[0], args[1])


@daftar("hapus_index")
def _handle_hapus_index(ctx, args):
    return list.hapus_index(args[0], args[1])


@daftar("balik")
def _handle_balik(ctx, args):
    return list.balik(args[0])


# =====================================================
# 17. BILANGAN
# =====================================================


@daftar("bilangan_prima")
def _handle_bilangan_prima(ctx, args):
    return bilangan.bilangan_prima(args[0])


@daftar("bilangan_ganjil")
def _handle_bilangan_ganjil(ctx, args):
    return bilangan.bilangan_ganjil(args[0])


@daftar("bilangan_genap")
def _handle_bilangan_genap(ctx, args):
    return bilangan.bilangan_genap(args[0])


@daftar("bilangan_negatif")
def _handle_bilangan_negatif(ctx, args):
    return bilangan.bilangan_negatif(args[0])


@daftar("bilangan_pecahan")
def _handle_bilangan_pecahan(ctx, args):
    return bilangan.bilangan_pecahan(args[0])


@daftar("bilangan_fibonacci")
def _handle_bilangan_fibonacci(ctx, args):
    return bilangan.bilangan_fibonacci(args[0])


@daftar("cek_bilangan")
def _handle_cek_bilangan(ctx, args):
    return bilangan.cek_bilangan(args[0])


@daftar("pi")
def _handle_pi(ctx, args):
    digits = args[0] if args else 2
    return bilangan.pi(digits)


# =====================================================
# 18. MATEMATIKA LANJUTAN
# =====================================================


@daftar("log")
def _handle_log(ctx, args):
    return (
        matematika.log(args[0], args[1]) if len(args) > 1 else matematika.log(args[0])
    )


@daftar("exp")
def _handle_exp(ctx, args):
    return matematika.exp(args[0])


@daftar("floor")
def _handle_floor(ctx, args):
    return matematika.floor(args[0])


@daftar("ceil")
def _handle_ceil(ctx, args):
    return matematika.ceil(args[0])


# =====================================================
# 19. LAINNYA
# =====================================================


@daftar("jumlah")
def _handle_jumlah(ctx, args):
    return lainya.jumlah(ctx, args)


@daftar("ada")
def _handle_ada(ctx, args):
    return lainya.ada(ctx, args)


@daftar("semua")
def _handle_semua(ctx, args):
    return lainya.semua(ctx, args)


@daftar("himpunan")
def _handle_himpunan(ctx, args):
    return lainya.himpunan(ctx, args)


# =====================================================
# 20. API (REST Client)
# =====================================================


@daftar("ambil_data_api")
def _handle_ambil_data_api(ctx, args):
    return ambil_data_api(
        args[0] if len(args) > 0 else None,
        _sumber=args[1] if len(args) > 1 else "api_url",
        headers=args[2] if len(args) > 2 else None,
        halaman=args[3] if len(args) > 3 else None,
        batas=args[4] if len(args) > 4 else None,
        params=args[5] if len(args) > 5 else None,
        context=ctx,
    )


@daftar("kirim_data_api")
def _handle_kirim_data_api(ctx, args):
    return kirim_data_api(
        args[0] if len(args) > 0 else None,
        args[1] if len(args) > 1 else None,
        args[2] if len(args) > 2 else None,
        context=ctx,
    )


@daftar("perbarui_data_api")
def _handle_perbarui_data_api(ctx, args):
    return perbarui_data_api(
        args[0] if len(args) > 0 else None,
        args[1] if len(args) > 1 else {},
        headers=args[2] if len(args) > 2 else None,
        context=ctx,
    )


@daftar("hapus_data_api")
def _handle_hapus_data_api(ctx, args):
    return hapus_data_api(
        args[0] if len(args) > 0 else None,
        headers=args[1] if len(args) > 1 else None,
        context=ctx,
    )


@daftar("cari_data_api")
def _handle_cari_data_api(ctx, args):
    data = args[0] if len(args) > 0 else []
    query = args[1] if len(args) > 1 else {}
    if not isinstance(query, dict):
        query = {}
    return cari_data_api(data, **query)


@daftar("simpan_data_api")
def _handle_simpan_data_api(ctx, args):
    return simpan_data_api(
        args[0] if len(args) > 0 else None,
        filename=args[1] if len(args) > 1 else "data_api.json",
        folder=args[2] if len(args) > 2 else "data",
    )


@daftar("parse_json_api")
def _handle_parse_json_api(ctx, args):
    return parse_json_api(
        args[0] if len(args) > 0 else None, args[1] if len(args) > 1 else ""
    )


@daftar("cek_data_api")
def _handle_cek_data_api(ctx, args):
    return cek_data_api(
        args[0] if len(args) > 0 else "",
        timeout=args[1] if len(args) > 1 else 5,
        context=ctx,
    )


# =====================================================
# CALL METHOD — Untuk method chaining pada objek
# =====================================================


def call_method(context, obj_tarri, method_name, args_tarri):
    """Memanggil method pada objek Python dari konteks TARRI."""
    obj_py = obj_tarri
    args_py = [context.translate_to_python(a) for a in args_tarri]

    try:
        method = getattr(obj_py, method_name)
        result_py = method(*args_py)

        if result_py is None:
            return None
        elif result_py is True:
            return True
        elif result_py is False:
            return False
        return result_py

    except AttributeError:
        context.error(
            f"Metode '{method_name}' tidak ditemukan pada objek '{obj_py.__class__.__name__}'."
        )
        return None
    except Exception as e:
        context.error(f"Eksekusi metode '{method_name}' gagal: {e}")
        return None


# =====================================================
# CALL FUNCTION — Dispatcher utama (sekarang ringkas!)
# =====================================================


def call_function(self, func_name, args):
    """Dispatcher utama untuk semua fungsi built-in TARRI.

    Menggunakan dispatch table BUILTINS untuk lookup O(1)
    alih-alih rantai elif O(n).
    """
    # 1. Handle literal boolean/null
    if isinstance(func_name, bool):
        return func_name

    if isinstance(func_name, str):
        name = func_name
    else:
        name = str(func_name)

    # 2. Handle literal values
    name_lower = name.lower()
    if name_lower in ("benar", "salah"):
        return name_lower == "benar"
    if name_lower == "null":
        return None

    # 3. Lookup di dispatch table — O(1)
    handler = BUILTINS.get(func_name)
    if handler:
        return handler(self, args)

    # 4. Cek fungsi user-defined
    if func_name in getattr(self, "functions", {}):
        return self.exec_func_call(func_name, args)

    # 5. Handle list (edge case)
    if isinstance(func_name, builtins.list):
        func_name = ".".join(str(x) for x in func_name if x)
        return None

    # 6. Fungsi tidak ditemukan
    if func_name in ("cetak",):
        self.error(
            f"Fungsi '{func_name}' dipanggil, tapi tidak berada di blok titikawal{{ ... }}!"
        )
    else:
        self.error(f"Fungsi '{func_name}' tidak ditemukan")

    return None
