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


def masukkan(interpreter, args):
    """
    Fungsi masukkan() untuk bahasa Tarri.
    interpreter : instance interpreter (buat akses context)
    args        : argumen dari AST
    """
    raw_var = args[0]
    if isinstance(raw_var, Token):
        var_name = raw_var.value
    elif isinstance(raw_var, Tree) and raw_var.data == "identifier":
        first = raw_var.children[0]
        var_name = first.value if isinstance(first, Token) else str(first)
    else:
        var_name = str(raw_var)

    prompt = args[1] if len(args) > 1 else ""
    expect_type = None

    # cek apakah ada type_cast
    if hasattr(args[0], "data") and args[0].data == "type_cast":
        var_name_node = args[0].children[0]
        cast_token = args[0].children[1]
        expect_type = cast_token.value
        var_name = var_name_node.value if isinstance(var_name_node, Token) else str(var_name_node)

    # hanya ambil input user, jangan pernah cast var_name!
    value = input(prompt).strip()

    # ==== AUTO KONVERSI (hanya untuk 'value') ====
    if expect_type == "angka":
        try:
            value = int(value) if "." not in value else float(value)
        except ValueError:
            print(f"[tarri] input ({var_name}) hanya bisa menerima tipe data angka.")
            return None

    elif expect_type == "desimal":
        try:
            value = float(value)
        except ValueError:
            print(f"[tarri] input ({var_name}) hanya bisa menerima tipe data desimal.")
            return None

    elif expect_type == "kata":
        value = str(value)

    else:
        # AUTO DETEKSI TIPE dari input user
        lower_val = value.lower()

        if lower_val in ("benar", "true"):
            value = True
        elif lower_val in ("salah", "false"):
            value = False
        elif lower_val in ("kosong", "hampa", "null", "none"):
            value = None
        elif value.replace(".", "", 1).isdigit():
            try:
                value = int(value) if "." not in value else float(value)
            except ValueError:
                value = str(value)
        else:
            value = str(value)

    # simpan hasil input user ke context
    interpreter.context[var_name] = value

    # optional: debug, langsung kasih tahu tipe input
    # print(f"[tarri] ({var_name}) terdeteksi tipe: {tipe_data(value)}")

    return None
