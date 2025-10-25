# from lark import Tree, Token

# def tipe_data(val):
#     if isinstance(val, bool):
#         return "logika"
#     elif isinstance(val, (int, float)):
#         return "angka"
#     elif isinstance(val, str):
#         return "kata"
#     elif val is None:
#         return "kosong"
#     else:
#         return "tak dikenal"


# def paksa_angka(val, var_name):
#     try:
#         if "." in str(val):
#             return float(val)
#         else:
#             return int(val)
#     except ValueError:
#         print(f"[tarri] masukkan ({var_name}) hanya bisa menerima angka.")
#         return None


# def paksa_kata(val, var_name):
#     val_str = str(val)
#     if not val_str.replace(" ", "").isalpha():
#         print(f"[tarri] masukkan ({var_name}) hanya bisa menerima kata.")
#         return None
#     return val_str


# def angka_str(val, var_name):
#     return str(val)


# def masukkan(interpreter, args):
#     raw_var = args[0]

#     # --- Mode literal (masukkan("Nama:")) ---
#     if isinstance(raw_var, Tree) and raw_var.data == "string":
#         string_token = raw_var.children[0]
#         prompt = string_token.value.strip('"').strip("'")
#         var_name = "_masukan_terakhir"
#     # --- Mode variabel (masukkan(_nama)) ---
#     elif isinstance(raw_var, Token):
#         var_name = raw_var.value
#         prompt = f"Masukkan nilai untuk '{var_name.lstrip('_')}'"
#     elif isinstance(raw_var, Tree) and raw_var.data == "identifier":
#         first = raw_var.children[0]
#         var_name = first.value if isinstance(first, Token) else str(first)
#         prompt = f"Masukkan nilai untuk '{var_name.lstrip('_')}'"
#     else:
#         var_name = "_masukan_terakhir"
#         prompt = str(raw_var)

#     # --- Argumen kedua opsional ---
#     if len(args) > 1:
#         extra = args[1]
#         if isinstance(extra, Tree) and extra.data == "string":
#             prompt += " " + extra.children[0].value.strip('"').strip("'")
#         else:
#             prompt += " " + str(extra)

#     print(f"\n{prompt}")
#     value = input("> ").strip()

#     # --- Auto deteksi tipe ---
#     lower_val = value.lower()
#     if lower_val in ("benar", "true"):
#         value = True
#     elif lower_val in ("salah", "false"):
#         value = False
#     elif lower_val in ("kosong", "hampa", "null", "none"):
#         value = None

#     interpreter.context[var_name] = angka_str(value, var_name)

#     # --- Kalau di REPL, return langsung (tanpa wrapper) ---
#     if getattr(interpreter, "is_repl", False):
#         return value

#     # --- Wrapper chaining untuk pemanggilan langsung ---
#     class _InputWrapper:
#         def __init__(self, val, name, context):
#             self.val = val
#             self.var_name = name
#             self.context = context

#         def angka(self):
#             val2 = paksa_angka(self.val, self.var_name)
#             self.context[self.var_name] = val2
#             return val2

#         def kata(self):
#             val2 = paksa_kata(self.val, self.var_name)
#             self.context[self.var_name] = val2
#             return val2

#         def angka_str(self):
#             val2 = angka_str(self.val, self.var_name)
#             self.context[self.var_name] = val2
#             return val2

#         def __str__(self):
#             return str(self.val)

#     # --- Return wrapper, bukan nilai mentah ---
#     return _InputWrapper(value, var_name, interpreter.context)


from lark import Tree, Token

# ----------------------------
# Utility tipe data
# ----------------------------
def tipe_data(val):
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, (int, float)):
        return "angka"
    elif isinstance(val, str):
        return "kata"
    elif val is None:
        return "kosong"
    else:
        return "tak dikenal"

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
    return str(val)

# ----------------------------
# Fungsi masukkan fleksibel
# ----------------------------
def masukkan(interpreter, args):
    raw_var = args[0]

    # Tentukan prompt & nama variabel
    if isinstance(raw_var, Tree) and raw_var.data == "string":
        string_token = raw_var.children[0]
        prompt = string_token.value.strip('"').strip("'")
        var_name = "_masukan_terakhir"
    elif isinstance(raw_var, Token):
        var_name = raw_var.value
        prompt = f"Masukkan nilai untuk '{var_name.lstrip('_')}'"
    elif isinstance(raw_var, Tree) and raw_var.data == "identifier":
        first = raw_var.children[0]
        var_name = first.value if isinstance(first, Token) else str(first)
        prompt = f"Masukkan nilai untuk '{var_name.lstrip('_')}'"
    else:
        var_name = "_masukan_terakhir"
        prompt = str(raw_var)

    # Argumen kedua opsional untuk menambahkan keterangan
    if len(args) > 1:
        extra = args[1]
        if isinstance(extra, Tree) and extra.data == "string":
            prompt += " " + extra.children[0].value.strip('"').strip("'")
        else:
            prompt += " " + str(extra)

    print(f"\n{prompt}")
    value = input("> ").strip()

    # Deteksi otomatis tipe boolean/kosong
    lower_val = value.lower()
    if lower_val in ("benar", "true"):
        value = True
    elif lower_val in ("salah", "false"):
        value = False
    elif lower_val in ("kosong", "hampa", "null", "none"):
        value = None

    # Simpan dulu sebagai string di context untuk kompatibilitas
    interpreter.context[var_name] = angka_str(value, var_name)

    # Kalau di REPL, return langsung
    if getattr(interpreter, "is_repl", False):
        return value

    # ----------------------------
    # Wrapper fleksibel
    # ----------------------------
    class _InputWrapper:
        def __init__(self, val, name, context):
            self.val = val
            self.var_name = name
            self.context = context

        # Type casting chaining
        def angka(self):
            val2 = paksa_angka(self.val, self.var_name)
            self.context[self.var_name] = val2
            self.val = val2
            return val2

        def kata(self):
            val2 = paksa_kata(self.val, self.var_name)
            self.context[self.var_name] = val2
            self.val = val2
            return val2

        def angka_str(self):
            val2 = angka_str(self.val, self.var_name)
            self.context[self.var_name] = val2
            self.val = val2
            return val2

        def __iter__(self):
            # memungkinkan digunakan dalam loop for
            try:
                return iter(self.val)
            except TypeError:
                return iter(str(self.val))

        def __str__(self):
            return str(self.val)

        def __repr__(self):
            return f"<InputWrapper {self.var_name}={self.val}>"

    return _InputWrapper(value, var_name, interpreter.context)
