# kelola_api/parse_json_api.py

def parse_json_api(data, field_path):
    """
    Ambil nilai dari JSON/dict berdasarkan path field.

    Args:
        data (dict | list): JSON/dict asli dari API.
        field_path (str): Path ke field, pisahkan dengan titik, misal "user.name".

    Returns:
        any: Nilai field yang diminta, atau None jika tidak ada.
    """
    fields = field_path.split(".")
    result = data

    try:
        for f in fields:
            if isinstance(result, list):
                # jika field berupa angka untuk index list
                idx = int(f)
                result = result[idx]
            elif isinstance(result, dict):
                result = result.get(f)
            else:
                return None
        return result
    except (KeyError, IndexError, ValueError, TypeError):
        return None
