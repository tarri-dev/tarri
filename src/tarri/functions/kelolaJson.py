import os
import json
from typing import Any

# ==========================
# 🔹 Fungsi JSON Tarri
# ==========================

def buat_json(data: Any, indent: int = 4) -> str:
    """
    Mengubah Python dict/list menjadi string JSON.
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return f"Gagal membuat JSON: {e}"


def baca_json(file_path: str) -> Any:
    """
    Membaca file JSON dari folder dan mengembalikannya sebagai string JSON rapi.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # kembalikan string JSON rapi
            return json.dumps(data, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        return f"Gagal membaca JSON: File '{file_path}' tidak ditemukan"
    except json.JSONDecodeError as e:
        return f"Gagal membaca JSON: {e}"

    
def simpan_json(data, lokasi_file, nama_file, indent=4):
    try:
        # buat folder jika belum ada
        os.makedirs(lokasi_file, exist_ok=True)
        path = f"{lokasi_file}/{nama_file}"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return f"Data berhasil disimpan di {path}"
    except Exception as e:
        return f"Gagal menyimpan JSON: {e}"