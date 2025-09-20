from lark import Tree, Token

def tipe_data(val):
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, int) or isinstance(val, float):
        return "angka"
    elif isinstance(val, str):
        return "kata"
    elif val is None:
        return "kosong"
    else:
        return "tak dikenal"

# paksa tipe
def paksa_angka(val, var_name):
    try:
        if "." in str(val):
            return float(val)
        else:
            return int(val)
    except ValueError:
        print(f"[tarri] masukkan ({var_name}) hanya bisa menerima angka.")
        return None

def paksa_kata(val, var_name):
    val_str = str(val)
    if not val_str.replace(" ", "").isalpha():
        print(f"[tarri] masukkan ({var_name}) hanya bisa menerima kata.")
        return None
    return val_str

def angka_str(val, var_name):
    """Simpan angka sebagai string literal, nol di depan tetap ada"""
    return str(val)

def masukkan(interpreter, args):
    raw_var = args[0]
    if isinstance(raw_var, Token):
        var_name = raw_var.value
    elif isinstance(raw_var, Tree) and raw_var.data == "identifier":
        first = raw_var.children[0]
        var_name = first.value if isinstance(first, Token) else str(first)
    else:
        var_name = str(raw_var)

    prompt = args[1] if len(args) > 1 else ""

    # --- Tampilan minimalis tanpa underscore di awal ---
    print(f"\nMasukkan nilai untuk '{var_name.lstrip('_')}'")
    value = input(f"{prompt}> ").strip()

    # --- AUTO DETEKSI TIPE ---
    lower_val = value.lower()
    if lower_val in ("benar", "true"):
        value = True
    elif lower_val in ("salah", "false"):
        value = False
    elif lower_val in ("kosong", "hampa", "null", "none"):
        value = None
    else:
        value = value  # tetap string literal (angka_str default)

    # --- Simpan ke context ---
    interpreter.context[var_name] = angka_str(value, var_name)

    # --- Dukungan chaining ---
    class _InputWrapper:
        def __init__(self, val, name, context):
            self.val = val
            self.var_name = name
            self.context = context

        def angka(self):
            val2 = paksa_angka(self.val, self.var_name)
            self.context[self.var_name] = val2
            return val2

        def kata(self):
            val2 = paksa_kata(self.val, self.var_name)
            self.context[self.var_name] = val2
            return val2

        def angka_str(self):
            val2 = angka_str(self.val, self.var_name)
            self.context[self.var_name] = val2
            return val2

    return _InputWrapper(value, var_name, interpreter.context)
