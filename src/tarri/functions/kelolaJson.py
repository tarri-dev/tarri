import os
import json

def simpanJson(filename, data):
    """Menyimpan data ke file JSON (overwrite)"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def bacaJson(filename):
    """Membaca file JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def perbaruiJson(filename, data):
    """Memperbarui file JSON dengan data baru"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {}

    if isinstance(old_data, dict) and isinstance(data, dict):
        old_data.update(data)
    elif isinstance(old_data, list) and isinstance(data, list):
        old_data.extend(data)
    else:
        # kalau format beda, langsung timpa aja
        old_data = data

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)

    return True


def hapusJson(filename):
    """Menghapus file JSON"""
    try:
        os.remove(filename)
        return True
    except FileNotFoundError:
        return False
