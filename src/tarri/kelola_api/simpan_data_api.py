# kelola_api/simpan_data_api.py

import json
import os

def simpan_data_api(data, filename="data_api.json", folder="data"):
    """
    Simpan data (dictionary atau list) ke file JSON.

    Args:
        data (dict | list): Data yang akan disimpan.
        filename (str, optional): Nama file JSON. Default "data_api.json".
        folder (str, optional): Folder tempat menyimpan file. Default "data".
    
    Returns:
        str: Path file hasil simpan.
    """
    # buat folder jika belum ada
    os.makedirs(folder, exist_ok=True)
    
    filepath = os.path.join(folder, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return filepath
    except Exception as e:
        return f"Error menyimpan data: {str(e)}"
