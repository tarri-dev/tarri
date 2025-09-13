import os

# ================= TXT =================
def simpanTxt(filename, content, ctx=None, tarri_file=None):
    """Menyimpan teks ke file (overwrite) relatif terhadap folder file .tarri"""
    try:
        base_path = os.path.dirname(tarri_file) if tarri_file else os.getcwd()
        full_path = os.path.join(base_path, filename)

        # Jika content adalah dict dengan format _key => value
        if isinstance(content, dict):
            lines = []
            for k, v in content.items():
                # Tambahkan tanda kutip untuk string, biarkan angka tetap
                if isinstance(v, str):
                    v = f'"{v}"'
                lines.append(f"{k} => {v}")
            content = "_data [\n    " + ",\n    ".join(lines) + "\n]"

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(str(content))

        if ctx is not None:
            ctx["i"] = "sukses disimpan"
        return True
    except FileNotFoundError:
        if ctx is not None:
            ctx["i"] = "gagal disimpan: folder atau path tidak ditemukan"
        return False
    except PermissionError:
        if ctx is not None:
            ctx["i"] = "gagal disimpan: akses ditolak"
        return False
    except Exception:
        if ctx is not None:
            ctx["i"] = "gagal disimpan: terjadi kesalahan"
        return False


def parse_txt_arrow_format(content, block_name=""):
    """Parse format _block_name [ _key => value, ... ] menjadi dict fleksibel"""
    data_dict = {}
    content = content.strip()
    start_idx = content.find(f"{block_name} [")
    end_idx = content.rfind("]")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        block = content[start_idx + len(f"{block_name} ["):end_idx]
        lines = block.splitlines()
        for line in lines:
            line = line.strip().rstrip(",")
            if "=>" in line:
                k, v = line.split("=>", 1)
                k = k.strip()
                v = v.strip()
                # Hilangkan tanda kutip jika ada
                if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                else:
                    # Coba cast ke int
                    try:
                        v = int(v)
                    except ValueError:
                        try:
                            v = float(v)
                        except ValueError:
                            pass
                data_dict[k] = v
        return data_dict if data_dict else None
    return None




def bacaTxt(filename, key=None, ctx=None, tarri_file=None):
    """Membaca file teks relatif terhadap folder file .tarri"""
    try:
        base_path = os.path.dirname(tarri_file) if tarri_file else os.getcwd()
        full_path = os.path.join(base_path, filename)

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        data_dict = parse_txt_arrow_format(content)

        if data_dict:
            result = data_dict.get(key) if key else data_dict
        else:
            result = content  # file biasa

        if ctx is not None:
            ctx["i"] = "sukses dibaca"
        return result
    except FileNotFoundError:
        if ctx is not None:
            ctx["i"] = "gagal dibaca: file tidak ditemukan"
        return None
    except PermissionError:
        if ctx is not None:
            ctx["i"] = "gagal dibaca: akses ditolak"
        return None
    except Exception as e:
        if ctx is not None:
            ctx["i"] = "gagal dibaca: terjadi kesalahan"
        return None


def perbaruiTxt(filename, content, ctx=None, tarri_file=None):
    """Menambah (append) teks ke file relatif terhadap folder file .tarri"""
    try:
        base_path = os.path.dirname(tarri_file) if tarri_file else os.getcwd()
        full_path = os.path.join(base_path, filename)

        if isinstance(content, dict):
            lines = []
            for k, v in content.items():
                if isinstance(v, str):
                    v = f'"{v}"'
                lines.append(f"{k} => {v}")
            content = "_data [\n    " + ",\n    ".join(lines) + "\n]\n"

        with open(full_path, "a", encoding="utf-8") as f:
            f.write(str(content))

        if ctx is not None:
            ctx["i"] = "sukses diperbarui"
        return True
    except FileNotFoundError:
        if ctx is not None:
            ctx["i"] = "gagal diperbarui: file atau folder tidak ditemukan"
        return False
    except PermissionError:
        if ctx is not None:
            ctx["i"] = "gagal diperbarui: akses ditolak"
        return False
    except Exception:
        if ctx is not None:
            ctx["i"] = "gagal diperbarui: terjadi kesalahan"
        return False


def hapusTxt(filename, ctx=None, tarri_file=None):
    """Menghapus file teks relatif terhadap folder file .tarri"""
    try:
        base_path = os.path.dirname(tarri_file) if tarri_file else os.getcwd()
        full_path = os.path.join(base_path, filename)

        os.remove(full_path)

        if ctx is not None:
            ctx["i"] = "sukses dihapus"
        return True
    except FileNotFoundError:
        if ctx is not None:
            ctx["i"] = "gagal dihapus: file tidak ditemukan"
        return False
    except PermissionError:
        if ctx is not None:
            ctx["i"] = "gagal dihapus: akses ditolak"
        return False
    except Exception:
        if ctx is not None:
            ctx["i"] = "gagal dihapus: terjadi kesalahan"
        return False


# titikawal{
#     _hasil = simpanTxt("/root/tes.txt", "coba")
    
#     jika(_hasil) {
#         cetak "sukses, {i}"
#     } lainnya {
#         cetak "gagal, {i}"
#     }
# }

# cara menggunakan kelolatxt()

# titikawal{
#     _data = bacaTxt("examples/txt_baru.txt")

#     _username = _data["_username"]
#     _sandi = _data["_sandi"]

#     cetak _username
#     cetak _sandi
# }


# bisa juga seperti ini


# titikawal{cetak "register akun baru"}

# masukkan(_masukkan_nama, "masukkan nama anda : ")
# masukkan(_masukkan_sandi, "masukkan sandi anda : ")

# _hash_sandi = buatSandi(_masukkan_sandi)
# _id = angkaAcak(10,100)

# titikawal{
    
#     simpanTxt("examples/akun.txt","
#         _akun [
#             _id     => {_id},
#             _nama   => {_masukkan_nama},
#             _sandi  => {_hash_sandi}
#         ]
#     ")

#     _akun = bacaTxt("examples/akun.txt")

#     _id         = _akun["_id"]
#     _nama       = _akun["_nama"]
#     _sandi      = _akun["_sandi"]


#     cetak _id "|" _nama "|" _sandi
    
# }


# hasilnya :
# register akun baru
# masukkan nama anda : dana
# masukkan sandi anda : dana
# 44 | dana | pIIckBgh$471cacd44307347aee505b018d5b7e878fbea3f68ee158d53ce9f0d9e17d6055ffda9359ff7cc8c4fdb1cb18abec99faf352db861414aba51baaf85d93937f44
