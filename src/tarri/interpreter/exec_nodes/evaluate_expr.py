#==============================================================================#
# File    : evaluate_expr.py                                                   #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Executor node untuk menerjemahkan dan mengeksekusi AST node bertipe        #
#   'evaluate_expr' dalam penerjemah Tarri.                                    #
#==============================================================================#

from lark import Tree, Token
from tarri.datatypes import DATATYPES
from tarri.functions.masukkan import paksa_angka, paksa_kata
import re


def evaluate_expr(self, node):

    if node is None:
        return None

    if isinstance(node, Tree):
        if node.data == "param" and node.children:
            child = node.children[0]
            return child.value if isinstance(child, Token) else str(child)

        if node.data == "grouped_expr":
            return self.evaluate_expr(node.children[0])

        elif node.data == "dict_literal":
            return self.exec_dict_literal(node)

        elif node.data == "null_coalesce":
            # Jika hanya 1 child, tidak ada operator ??, kembalikan langsung
            if len(node.children) < 2:
                return self.evaluate_expr(node.children[0]) if node.children else None

            # Evaluasi semua children secara berantai (mendukung Kosong ?? Kosong ?? "akhir")
            for child in node.children:
                val = self.evaluate_expr(child)
                is_null = val is None or str(val).lower() in [
                    "null", "none", "kosong", "hampa", ""
                ]
                if not is_null:
                    return val
            # Jika semua null, kembalikan nilai terakhir
            return self.evaluate_expr(node.children[-1])

        elif node.data == "method_chain":
            obj = self.evaluate_expr(node.children[0])
            method_name = node.children[1].value
            args = []
            if len(node.children) > 2:
                args_node = node.children[2]
                if args_node is not None:
                    args = [self.evaluate_expr(a) for a in args_node.children]
            if hasattr(obj, method_name):
                return getattr(obj, method_name)(*args)
            else:
                self.error(f"Objek tidak memiliki metode '{method_name}'")
                return None

        elif node.data == "type_cast":
            inner_val = self.evaluate_expr(node.children[0])
            cast_type = node.children[1].value

            # Duck typing
            if hasattr(inner_val, "angka") or hasattr(inner_val, "kata"):
                if cast_type == "angka":
                    return inner_val.angka()
                elif cast_type == "kata":
                    return inner_val.kata()
                else:
                    raise Exception(f"Tipe konversi '{cast_type}' tidak dikenali pada objek ini")
            else:
                # fallback: coba paksa langsung
                if cast_type == "angka":
                    return paksa_angka(inner_val, "cast")
                elif cast_type == "kata":
                    return paksa_kata(inner_val, "cast")

        elif node.data == "func_decl":
            return self.exec_func_decl(node)

        elif node.data == "call_expr":
            # type_cast inside call_expr handled here
            if (
                isinstance(node.children[0], Tree)
                and node.children[0].data == "type_cast"
            ):
                cast_node = node.children[0]
                inner_call = cast_node.children[0]
                cast_type_token = cast_node.children[1]
                cast_type = cast_type_token.value
                wrapper = self.evaluate_expr(inner_call)
                if cast_type == "angka":
                    # wrapper expected convertible
                    try:
                        return int(wrapper)
                    except Exception:
                        try:
                            return float(wrapper)
                        except Exception:
                            return wrapper
                elif cast_type == "kata":
                    return str(wrapper)

            func_node = node.children[0]
            if isinstance(func_node, Token):
                func_name = func_node.value
            elif (
                isinstance(func_node, Tree)
                and func_node.data == "identifier"
                and func_node.children
            ):
                first = func_node.children[0]
                func_name = first.value if isinstance(first, Token) else str(first)
            else:
                func_name = str(func_node)
            args_values = []

            if len(node.children) > 1:
                maybe_args = node.children[1]
                if isinstance(maybe_args, Tree) and maybe_args.data == "args":
                    for i, a in enumerate(maybe_args.children):
                        if func_name == "masukkan" and i == 0:
                            args_values.append(a)
                        else:
                            args_values.append(self.evaluate_expr(a))
                else:
                    for i, a in enumerate(node.children[1:]):
                        if func_name == "masukkan" and i == 0:
                            args_values.append(a)
                        else:
                            args_values.append(self.evaluate_expr(a))

            if func_name in self.functions:
                return self.exec_func_call(func_name, args_values)
            return self.call_function(func_name, args_values)

        elif node.data == "subcall_expr":

            # 1. Evaluasi target (Modul atau Objek)
            target = self.evaluate_expr(node.children[0])

            # 2. Ambil nama aksi/metode (misal: 'koneksi' atau 'buat')
            method_node = node.children[1]
            method_name = (
                method_node.value
                if isinstance(method_node, Token)
                else str(method_node)
            )

            # 3. Kumpulkan Argumen (Node 2, jika ada)
            args = []
            if len(node.children) > 2:
                args_node = node.children[2]
                if isinstance(args_node, Tree) and args_node.data == "args":
                    args = [self.evaluate_expr(a) for a in args_node.children]

            # --- DISPATCH BERDASARKAN TIPE TARGET ---

            # KASUS 1: Panggilan Fungsi Global (misal: 'sqlite koneksi')
            if isinstance(target, str):
                # Target adalah string (nama modul global). Kirim ke call_function lama.
                # Catatan: method_name ('koneksi') dijadikan argumen pertama untuk aksi.
                return self.call_function(target, [method_name] + args)

            # KASUS 2: Panggilan Metode Objek (misal: _pengguna buat)
            elif target is not None:
                # Target adalah objek (misal: SQLiteHandler). Panggil fungsi call_method baru.

                # Di sini, kita asumsikan Anda memiliki delegasi 'self.call_method' di kelas Context
                # yang menunjuk ke fungsi di exec_nodes/call_function.py

                try:
                    return self.call_method(target, method_name, args)
                except AttributeError as e:
                    self.error(
                        f"Objek '{self.stringify(target)}' tidak memiliki metode '{method_name}'."
                    )
                    return self.NIL_VALUE

            # KASUS 3: Target Null/Tidak Ditemukan
            # else:
            #     # Jika _pengguna tidak mendapatkan objek koneksi (misalnya gagal),
            #     # maka panggilan ini akan gagal.
            #     self.error(f"Target panggilan metode tidak valid: Nilai '{self.stringify(node.children[0])}' adalah null.")
            #     return self.NIL_VALUE
            else:
                target_name = self.stringify(node.children[0])
                line_info = ""
                if hasattr(node, "meta"):
                    line = getattr(node.meta, "line", None)
                    if line:
                        line_info = f" (baris: {line})"
                self.error(
                    f"Gagal memanggil metode: variabel '{target_name}' bernilai kosong{line_info}."
                )
                return self.NIL_VALUE

        elif node.data == "string":
            raw = node.children[0].value.strip('"')

            def replacer(match):
                expr_code = match.group(1).strip()

                if "[" in expr_code:
                    var_part, rest = expr_code.split("[", 1)
                    var_part = var_part.strip()
                    rest = rest.rstrip("]").strip()

                    if ".." in rest:  # slice
                        start_str, end_str = rest.split("..", 1)
                        start_str, end_str = start_str.strip(), end_str.strip()

                        # FIX: Bungkus ke Token, jangan evaluate dulu
                        start = (
                            Token("NUMBER", start_str)
                            if start_str.isdigit()
                            else Token("VAR_NAME", start_str)
                        )
                        end = (
                            Token("NUMBER", end_str)
                            if end_str.isdigit()
                            else Token("VAR_NAME", end_str)
                        )

                        sub_tree = Tree(
                            "indexing",
                            [
                                Token("VAR_NAME", var_part),
                                Tree("slice_expr", [start, end]),
                            ],
                        )
                    elif "&" in rest:  # pair
                        parts = []
                        for p in rest.split("&"):
                            p = p.strip()
                            # FIX: Bungkus ke Token
                            if p.isdigit():
                                parts.append(Token("NUMBER", p))
                            else:
                                parts.append(Token("VAR_NAME", p))

                        sub_tree = Tree(
                            "indexing",
                            [Token("VAR_NAME", var_part), Tree("pair_expr", parts)],
                        )
                    else:  # single
                        if rest.startswith(("'", '"')) and rest.endswith(("'", '"')):
                            key_val = rest[1:-1]
                            key_token = Token("ESCAPED_STRING", f'"{key_val}"')
                        elif rest.isdigit():
                            key_token = Token("NUMBER", rest)
                        else:
                            key_token = Token("VAR_NAME", rest)
                        sub_tree = Tree(
                            "indexing",
                            [
                                Token("VAR_NAME", var_part),
                                Tree("single_index", [key_token]),
                            ],
                        )

                else:
                    sub_tree = Tree("identifier", [Token("VAR_NAME", expr_code)])

                val = self.evaluate_expr(sub_tree)
                return self.stringify(val, compact=True)

            text = re.sub(r"\{([^}]+)\}", replacer, raw)
            return DATATYPES["kata"](text)

        # elif node.data == "number":
        #     val = node.children[0].value
        #     return DATATYPES["angka"](val) if val.isdigit() else DATATYPES["desimal"](val)

        elif node.data == "number":
            val = node.children[0].value
            return int(val) if val.isdigit() else float(val)

        elif node.data == "list_literal":
            return [self.evaluate_expr(ch) for ch in node.children]

        elif node.data == "add_expr":
            left = self.evaluate_expr(node.children[0])
            right = self.evaluate_expr(node.children[2])
            op = node.children[1].value
            if op == "+":
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif op == "-":
                return left - right

        elif node.data == "method_call_expr":
            # expr_atom "->" NAME "(" [args] ")"
            obj = self.evaluate_expr(node.children[0])  # objek, misal sesi()
            method_name = node.children[1].value  # nama method
            args = []
            if len(node.children) > 2:
                args_node = node.children[2]
                if args_node is not None and isinstance(args_node, Tree):
                    args = [self.evaluate_expr(c) for c in args_node.children]

            if hasattr(obj, method_name):
                method = getattr(obj, method_name)
                if callable(method):
                    return method(*args)
                else:
                    raise Exception(
                        f"'{method_name}' adalah atribut, bukan metode pada objek {type(obj).__name__}"
                    )
            else:
                raise Exception(f"Objek {type(obj).__name__} tidak memiliki metode '{method_name}'")

        elif node.data == "mul_expr":
            left = self.evaluate_expr(node.children[0])
            right = self.evaluate_expr(node.children[2])
            op = node.children[1].value
            if op == "*":
                return left * right
            elif op == "/":
                return left / right
            elif op == "%":
                return left % right

        elif node.data == "not_expr":
            value = self.evaluate_expr(node.children[0])
            return not bool(value)

        elif node.data == "compare_expr":
            left = self.evaluate_expr(node.children[0])
            op = node.children[1].value
            right = self.evaluate_expr(node.children[2])
            return self.compare(op, left, right)

        # AND (&&)
        elif node.data == "and_expr":
            left = self.evaluate_expr(node.children[0])
            if not bool(left):
                return False
            right = self.evaluate_expr(node.children[-1])
            return bool(right)

        # OR (||)
        elif node.data == "or_expr":
            left = self.evaluate_expr(node.children[0])
            if bool(left):
                return True
            right = self.evaluate_expr(node.children[-1])
            return bool(right)

        elif node.data == "in_expr":
            kiri = self.evaluate_expr(node.children[0])
            kanan = self.evaluate_expr(node.children[1])

            try:
                return kiri in kanan
            except TypeError:
                return False

        elif node.data == "identifier":
            name_token = node.children[0]
            name = (
                name_token.value if isinstance(name_token, Token) else str(name_token)
            )
            line = name_token.line if isinstance(name_token, Token) else None

            # 1. Cari nama aslinya dulu
            return self.get_var(name, node=name_token)

        elif node.data == "indexing":
            # Ambil objek
            obj_node = node.children[0]
            idx_node = node.children[1]

            if isinstance(obj_node, Token):
                obj_name = obj_node.value
                if obj_name not in self.context:
                    self.error(f"Variabel '{obj_name}' tidak ditemukan")
                    return None
                obj = self.context[obj_name]
            else:
                obj = self.evaluate_expr(obj_node)

            # SINGLE INDEX: kembalikan elemen tunggal
            if idx_node.data == "single_index":
                index_val = self.evaluate_expr(idx_node.children[0])
                try:
                    if isinstance(obj, dict):
                        return obj.get(index_val)
                    else:
                        return obj[int(index_val)]
                except (IndexError, KeyError, TypeError):
                    self.error(f"Indeks {index_val} di luar jangkauan pada '{obj_name}' (panjang: {len(obj) if hasattr(obj, '__len__') else '?'})")
                    return None

            # SLICE EXPR: selalu kembalikan sublist
            elif idx_node.data == "slice_expr":
                start_node = (
                    idx_node.children[0] if len(idx_node.children) > 0 else None
                )
                end_node = idx_node.children[1] if len(idx_node.children) > 1 else None

                start = self.evaluate_expr(start_node) if start_node else 0
                end = self.evaluate_expr(end_node) if end_node else len(obj) - 1

                # fallback
                if start is None:
                    start = 0
                if end is None:
                    end = len(obj) - 1

                try:
                    start_int = int(start)
                    end_int = int(end)
                    # Tarri slice inclusive: end_int + 1
                    return obj[start_int : end_int + 1]
                except Exception as e:
                    self.error(f"Pemotongan (slice) gagal: mulai={start}, akhir={end}, kesalahan={e}")
                    return None

            # PAIR EXPR: selalu kembalikan list
            elif idx_node.data == "pair_expr":
                try:
                    raw_parts = [
                        str(self.evaluate_expr(ch)).strip()
                        for ch in idx_node.children
                        if ch is not None
                    ]

                    indices = []
                    i = 0
                    while i < len(raw_parts):
                        part = raw_parts[i]

                        # cek pattern start .. end (inclusive)
                        if (
                            re.match(r"^\d+$", part)
                            and i + 2 < len(raw_parts)
                            and raw_parts[i + 1] == ".."
                            and re.match(r"^\d+$", raw_parts[i + 2])
                        ):
                            start = int(part)
                            end = int(raw_parts[i + 2])
                            indices.extend(range(start, end + 1))
                            i += 3
                            continue

                        # cek single index
                        if part.isdigit():
                            indices.append(int(part))

                        i += 1

                    indices = sorted(set(indices))
                    result = [obj[i] for i in indices if 0 <= i < len(obj)]

                    # jangan flatten, selalu list
                    return result

                except Exception as e:
                    self.error(f"Pengambilan pasangan (pair) gagal: {e}")
                    return None

            else:
                self.error(f"Cara pengindeksan '{idx_node.data}' tidak dikenali")
                return None

        elif node.data == "type_cast":
            value = self.evaluate_expr(node.children[0])
            cast_type_token = node.children[1]
            cast_type = cast_type_token.value
            if cast_type == "angka":
                try:
                    if "." in str(value):
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    self.error(f"Nilai '{value}' tidak dapat dikonversi menjadi angka")
                    return None
            elif cast_type == "kata":
                return str(value)
            else:
                self.error(f"Jenis konversi tidak dikenali: '{cast_type}'")
                return value

        elif node.data == "true":
            return True

        elif node.data == "false":
            return False

        elif node.data == "null":
            return None

        self.error(
            f"[tarri] Tidak dapat mengevaluasi ekspresi bertipe '{node.data}'"
        )
        return None

    elif isinstance(node, Token):

        if node.type == "VAR_NAME":
            return self.get_var(node.value)

        # elif node.type == "NUMBER":
        #     return DATATYPES["angka"](node.value) if node.value.isdigit() else DATATYPES["desimal"](node.value)

        elif isinstance(node, Token) and node.type == "NUMBER":
            return int(node.value) if node.value.isdigit() else float(node.value)

        elif node.type == "ESCAPED_STRING":
            raw = node.value.strip('"')

            def replacer(match):
                expr_code = match.group(1).strip()

                if "[" in expr_code:
                    var_part, rest = expr_code.split("[", 1)
                    var_part = var_part.strip()
                    rest = rest.rstrip("]").strip()

                    if ".." in rest:  # slice
                        start_str, end_str = rest.split("..", 1)
                        start_str, end_str = start_str.strip(), end_str.strip()

                        # FIX: Bungkus ke Token
                        start = (
                            Token("NUMBER", start_str)
                            if start_str.isdigit()
                            else Token("VAR_NAME", start_str)
                        )
                        end = (
                            Token("NUMBER", end_str)
                            if end_str.isdigit()
                            else Token("VAR_NAME", end_str)
                        )

                        sub_tree = Tree(
                            "indexing",
                            [
                                Token("VAR_NAME", var_part),
                                Tree("slice_expr", [start, end]),
                            ],
                        )
                    elif "&" in rest:  # pair
                        parts = []
                        for p in rest.split("&"):
                            p = p.strip()
                            # FIX: Bungkus ke Token
                            if p.isdigit():
                                parts.append(Token("NUMBER", p))
                            else:
                                parts.append(Token("VAR_NAME", p))

                        sub_tree = Tree(
                            "indexing",
                            [Token("VAR_NAME", var_part), Tree("pair_expr", parts)],
                        )
                    else:  # single
                        if rest.startswith(("'", '"')) and rest.endswith(("'", '"')):
                            key_val = rest[1:-1]
                            key_token = Token("ESCAPED_STRING", f'"{key_val}"')
                        elif rest.isdigit():
                            key_token = Token("NUMBER", rest)
                        else:
                            key_token = Token("VAR_NAME", rest)
                        sub_tree = Tree(
                            "indexing",
                            [
                                Token("VAR_NAME", var_part),
                                Tree("single_index", [key_token]),
                            ],
                        )

                else:
                    sub_tree = Tree("identifier", [Token("VAR_NAME", expr_code)])

                val = self.evaluate_expr(sub_tree)
                return self.stringify(val, compact=True)

            text = re.sub(r"\{([^}]+)\}", replacer, raw)
            return DATATYPES["kata"](text)
        else:
            return node.value
    return None
