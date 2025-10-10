# =====================================================
# call_function.py - Handler fungsi built-in TARRI
# =====================================================

from tarri.functions.kata_acak import kata_acak
from tarri.functions.lorem_ipsum import lorem_ipsum
from tarri.functions.angka_acak import angka_acak
from tarri.functions.uuid import UUID
from tarri.functions.slug import slug
from tarri.functions.tipedata import tipedata
from tarri.functions.masukkan import masukkan
from tarri.functions.cari_data import cari_data
from tarri.functions.termasuk import termasuk
from tarri.functions.halaman import halaman
from tarri.functions.tujuan import tujuan
from tarri.functions.rute import rute
from tarri.functions.cetak_henti import cetak_henti
from tarri.functions.lacak import lacak
from tarri.functions.kata_bijak import kata_bijak
from tarri.functions.sandi import buat_sandi, cek_sandi
from tarri.functions.kelolaTxt import simpanTxt, bacaTxt, perbaruiTxt, hapusTxt

# database
from tarri.database.buatbasisdata import BuatBasisData
from tarri.database.buattabel import BasisData, BuatTabel, HapusTabel
from tarri.database.permintaan import simpan, ambil, semua, rapi, dimana, atau_dimana, dan_dimana, ubah, hapus, pilih, pertama, batasi, urutkan

# support
from tarri.support import waktu, teks, matematika, waktu_proses

# sesi
from tarri.session.sesi import sesi as sesi_py


def call_function(self, func_name, args):
    """Eksekusi fungsi built-in TARRI berdasarkan nama"""

    # =====================================================
    # Database / Permintaan
    # =====================================================
    if func_name in ("simpan","ambil","semua","dimana","rapi","atau_dimana","dan_dimana","ubah","hapus","pilih","pertama","batasi","urutkan"):
        try:
            if func_name == "simpan":
                return simpan(*args)
            
            elif func_name == "ambil":
                bd_lokasi, bd_nama, tabel_nama = args[:3]
                method = args[3] if len(args) > 3 else "semua"
                extra_args = args[4:]
                ambil(bd_lokasi, bd_nama, tabel_nama)
                if method == "semua":
                    return semua()
                elif method == "dimana" and len(extra_args) >= 2:
                    kolom, nilai = extra_args[:2]
                    dimana(kolom, nilai)
                    return semua()
                elif method == "atau_dimana" and len(extra_args) >= 2:
                    kolom, nilai = extra_args[:2]
                    atau_dimana(kolom, nilai)
                    return semua()
                elif method == "dan_dimana" and len(extra_args) >= 2:
                    kolom, nilai = extra_args[:2]
                    dan_dimana(kolom, nilai)
                    return semua()
                else:
                    return "gagal: method tidak dikenali"

            elif func_name == "ubah":
                bd_lokasi, bd_nama, tabel_nama, data_baru = args[:4]
                ubah(bd_lokasi, bd_nama, tabel_nama, data_baru)
                if len(args) >= 6 and args[4] == "dimana":
                    kolom, nilai = args[5:7]
                    return dimana(kolom, nilai)
                return "gagal: ubah perlu 'dimana'"

            elif func_name == "hapus":
                bd_lokasi, bd_nama, tabel_nama = args[:3]
                dummy_data = args[3] if len(args) > 3 else None
                hapus(bd_lokasi, bd_nama, tabel_nama, dummy_data)
                if len(args) >= 5 and args[4] == "dimana":
                    kolom, nilai = args[5:7]
                    return dimana(kolom, nilai)
                return "gagal: hapus perlu 'dimana'"

            elif func_name == "semua":
                return semua()
            elif func_name == "dimana":
                return dimana(args[0], args[1])
            elif func_name == "atau_dimana":
                return atau_dimana(args[0], args[1])
            elif func_name == "dan_dimana":
                return dan_dimana(args[0], args[1])
            elif func_name == "rapi":
                return rapi(*args)
            elif func_name == "pilih":
                return pilih(*args)
            elif func_name == "pertama":
                return pertama()
            elif func_name == "batasi":
                return batasi(args[0])
            elif func_name == "urutkan":
                return urutkan(args[0])
        except Exception as e:
            print(f"[tarri | interpreter] kesalahan: {e}")
            return "gagal"

    # =====================================================
    # Fungsi Input / Utility
    # =====================================================
    if func_name == "masukkan":
        return masukkan(self, args)
    elif func_name == "cari_data":
        return cari_data(self, args)
    elif func_name == "termasuk":
        return termasuk(self, args)
    elif func_name == "rute":
        return rute(self, args)
    elif func_name == "tujuan":
        return tujuan(args)
    elif func_name == "halaman":
        return halaman(self, args)
    elif func_name == "sesi":
        return sesi_py(self, args)
    elif func_name == "cetak_henti":
        return cetak_henti(self, args)
    elif func_name == "lacak":
        return lacak(self, args)

    # =====================================================
    # Database Object / Blueprint
    # =====================================================
    elif func_name == "BuatBasisData":
        hasil, pesan = BuatBasisData(*args)
        self.context["i"] = pesan
        try:
            from tarri.database import buattabel
            buattabel.set_db_context(self.context)
        except Exception as e:
            print(f"[WARN] gagal inject context ke buattabel: {e}")
        return hasil
    elif func_name == "BasisData":
        return BasisData()
    elif func_name == "BuatTabel":
        hasil, pesan = BuatTabel(args[0])
        self.context["i"] = pesan
        return hasil
    elif func_name == "HapusTabel":
        if len(args) == 2:
            return HapusTabel(args[0], args[1])
        elif len(args) == 3:
            return HapusTabel(args[0], args[1], args[2])
        return "gagal"

    # =====================================================
    # Fungsi Random / Utility
    # =====================================================
    elif func_name == "kata_acak":
        return kata_acak(args[0] if args else 5)
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
    elif func_name == "tipedata":
        return tipedata(args[0])
    elif func_name == "buat_sandi":
        return buat_sandi(str(args[0]) if args else "")
    elif func_name == "cek_sandi":
        if len(args) < 2:
            self.error("cekSandi butuh 2 argumen: (password_plain, hash_salt)")
            return False
        return cek_sandi(args[0], args[1])

    # =====================================================
    # File / Text
    # =====================================================
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
    elif func_name == "jumlah":
        return matematika.jumlah(args[0])
    elif func_name == "median":
        return matematika.median(args[0])
    elif func_name == "variansi":
        return matematika.variansi(args[0])
    elif func_name == "std_dev":
        return matematika.std_dev(args[0])

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

    # =====================================================
    # Custom / Context function fallback
    # =====================================================
    elif func_name in getattr(self, "functions", {}):
        return self.exec_func_call(func_name, args)

    # jika built-in tapi dipanggil di luar titikawal
    elif func_name in ["cetak"]:
        self.error(f"Fungsi '{func_name}' dipanggil, tapi tidak berada di blok titikawal{{ ... }}!")
    else:
        self.error(f"Fungsi '{func_name}' tidak ditemukan")

    return None
