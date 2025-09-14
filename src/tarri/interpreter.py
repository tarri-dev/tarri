from lark import Tree, Token
from tarri.keywords import KEYWORDS
import tarri.keyword_list
from tarri.datatypes import DATATYPES
import tarri.datatypes_list
import re

from tarri.functions.kataAcak import kataAcak
from tarri.functions.angkaAcak import angkaAcak
from tarri.functions.uuid import UUID
from tarri.functions.tipedata import tipedata
from tarri.functions.masukkan import masukkan
from tarri.functions.sandi import buatSandi, cekSandi
from tarri.functions.kelolaTxt import simpanTxt, bacaTxt, perbaruiTxt, hapusTxt
from tarri.functions.kelolaJson import simpanJson, bacaJson, perbaruiJson, hapusJson







class Interpreter:

    # fungsi : Inisialisasi interpreter dengan context (variabel scope), status debug, fungsi yang terdefinisi, dan flag return
    def __init__(self, status=False):
        self.context = {}
        self.status = status
        self.functions = {}
        self._return_flag = None

    # fungsi : Mengeksekusi statement ekspresi dengan mengevaluasi child node pertama (jika ada)
    def exec_expr_stmt(self, node):
        if node.children:
            self.evaluate_expr(node.children[0])

    # fungsi : menampilkan error ke layar
    def error(self, msg):
        print(f"[tarri] {msg}")

    # fungsi :
    # Mengonversi context (variabel scope) menjadi dictionary dengan nilai yang sudah diubah ke string
    # Nilai None diubah menjadi string "null"
    # Berguna untuk debugging atau menampilkan state variabel dalam format yang mudah dibaca
    def _context_as_str_dict(self):
        return {k: (str(v) if v is not None else "null") for k, v in self.context.items()}

    # fungsi :
    # Mengonversi nilai menjadi string representation yang sesuai dengan bahasa yang diinterpretasi
    # Menangani nilai None sebagai "null"
    # Memformat array/list dengan bracket dan comma separator
    # Opsi compact untuk format yang lebih ringkas (tanpa spasi tambahan)
    def stringify(self, value, compact=False):
        if value is None:
            return "null"
        if isinstance(value, list):
            if compact:
                return ", ".join(self.stringify(v, compact=True) for v in value)
            else:
                return "[ " + ", ".join(self.stringify(v) for v in value) + " ]"
        return str(value)

    # fungsi :
    # Menjalankan program dengan mengeksekusi setiap statement dalam abstract syntax tree (AST) secara berurutan
    # Bertindak sebagai entry point utama untuk menjalankan seluruh program
    # Mengiterasi melalui semua child node dari root tree dan mengeksekusinya satu per satu
    def run(self, tree):
        for stmt in tree.children:
            self.exec_node(stmt)

    # Fungsi: Menjalankan semua statement dalam entry point program (biasanya fungsi main atau program utama)
    def exec_entry_point(self, node):
        for stmt in node.children:
            self.exec_node(stmt)

    # Fungsi: Menjalankan blok kode dengan pengecekan return statement
    # def exec_block(self, node):
    #     for stmt in node.children:
    #         if self._return_flag is not None:
    #             break
    #         self.exec_node(stmt)


    def exec_block(self, node):
        result = None
        for stmt in node.children:
            if self._return_flag is not None:
                break
            val = self.exec_node(stmt)
            # simpan result hanya jika statement ini return explicit
            if self._return_flag is not None:
                result = val
                break
        return result


    # Fungsi: Mendeklarasikan dan menginisialisasi variabel otomatis
    def exec_auto_var_decl(self, node):
        # node: VAR_NAME EQUAL expr
        var_name = node.children[0].value
        # value typically at index 2
        value_node = node.children[2] if len(node.children) > 2 else None
        value = self.evaluate_expr(value_node) if value_node is not None else None
        self.context[var_name] = value
        if self.status:
            print(f"[DEBUG] Assigned {var_name} = {value}")

    # fungsi : handling keywords 
    # memanggil semua keywords di dalam folder keywords untuk bisa diguakan didalam interpreter
    def exec_node(self, node):
        if not isinstance(node, Tree):
            return None

        if node.data in KEYWORDS:
            handler = KEYWORDS[node.data]
            return handler(self, node.children)

        handler_name = f"exec_{node.data}"
        if hasattr(self, handler_name):
            return getattr(self, handler_name)(node)

        self.error(f"Tidak tahu cara eksekusi {node.data}")
        return None

    # fungsi :
    # Mendeklarasikan dan menyimpan fungsi beserta parameter dan body-nya ke dalam dictionary functions untuk digunakan nanti.
    def exec_func_decl(self, node):
        # node: func_decl -> NAME, params, block
        func_name = node.children[0].value
        params_node = node.children[1] if len(node.children) > 1 else None
        params = []
        if isinstance(params_node, Tree) and params_node.data == "params":
            for p in params_node.children:
                # p is Tree("param") or Token
                if isinstance(p, Tree) and p.data == "param" and p.children:
                    child = p.children[0]
                    params.append(child.value if isinstance(child, Token) else str(child))
                elif isinstance(p, Token):
                    params.append(p.value)
        body = node.children[-1]
        self.functions[func_name] = (params, body)
        if self.status:
            print(f"[DEBUG] Fungsi '{func_name}' terdaftar dengan parameter {params}")

    # fungsi : 
    # Mengeksekusi statement pemanggilan fungsi dengan mengevaluasi argumen dan memanggil fungsi yang dimaksud.
    def exec_call_stmt(self, node):
        func_node = node.children[0]
        func_name = None
        if isinstance(func_node, Token):
            func_name = func_node.value
        elif isinstance(func_node, Tree) and func_node.data == "identifier" and func_node.children:
            first = func_node.children[0]
            func_name = first.value if isinstance(first, Token) else str(first)
        else:
            func_name = str(func_node)

        args = []
        if len(node.children) > 1:
            maybe_args = node.children[1]
            if isinstance(maybe_args, Tree) and maybe_args.data == "args":
                for a in maybe_args.children:
                    args.append(self.evaluate_expr(a))
            else:
                for a in node.children[1:]:
                    args.append(self.evaluate_expr(a))

        return self.call_function(func_name, args)

    def exec_return_stmt(self, node):
        if node.children:
            self._return_flag = self.evaluate_expr(node.children[0])
        else:
            self._return_flag = None
        return self._return_flag

    # Built-in function
    # def call_function(self, func_name, args):

    #     print(f"[DEBUG call_function] {func_name} args={args}")

    #     # fungsi kataAcak()
    #     if func_name == "kataAcak":
    #         length = args[0] if args else 5
    #         return kataAcak(length)

    #     # fungsi angkaAcak()
    #     if func_name == "angkaAcak":
    #         if len(args) == 2:
    #             return angkaAcak(args[0], args[1])
    #         elif len(args) == 1:
    #             return angkaAcak(0, args[0])
    #         else:
    #             return angkaAcak()

    #     # fungsi UUID()
    #     if func_name == "UUID":
    #         return UUID()

    #     #fungsi sandi()
    #     if func_name == "buatSandi":
    #         val = self.evaluate_expr(args[0])
    #         return buatSandi(val)

    #     # if func_name == "cekSandi":
    #     #     plain = self.evaluate_expr(args[0])
    #     #     hashed = self.evaluate_expr(args[1])
    #     #     return cekSandi(plain, hashed)

    #     if func_name == "cekSandi":
    #         plain = self.evaluate_expr(args[0])
    #         hashed = self.evaluate_expr(args[1])
            
    #         print(f"[DEBUG] cekSandi plain={repr(plain)} hashed={repr(hashed)}")
    #         result = cekSandi(plain, hashed)
    #         print(f"[DEBUG] result={result}")
    #         return result



    #     if func_name == "masukkan":
    #         # var_name = args[0]
    #         raw_var = args[0]
    #         if isinstance(raw_var, Token):
    #             var_name = raw_var.value
    #         elif isinstance(raw_var, Tree) and raw_var.data == "identifier":
    #             first = raw_var.children[0]
    #             var_name = first.value if isinstance(first, Token) else str(first)
    #         else:
    #             var_name = str(raw_var)

    #         prompt = args[1] if len(args) > 1 else ""
    #         expect_type = None

    #         # cek apakah ada type_cast
    #         if hasattr(args[0], "data") and args[0].data == "type_cast":
    #             var_name_node = args[0].children[0]
    #             cast_token = args[0].children[1]
    #             expect_type = cast_token.value
    #             var_name = var_name_node.value if isinstance(var_name_node, Token) else str(var_name_node)

    #         value = input(prompt)

    #         if expect_type == "angka":
    #             try:
    #                 if "." in value:
    #                     value = float(value)
    #                 else:
    #                     value = int(value)
    #             except ValueError:
    #                 print()
    #                 print(f"[tarri] input ({var_name}) hanya bisa menerima tipe data angka.")
    #                 return None

    #         elif expect_type == "desimal":
    #             try:
    #                 value = float(value)
    #             except ValueError:
    #                 print()
    #                 print(f"[tarri] input ({var_name}) hanya bisa menerima tipe data desimal.")
    #                 return None

    #         elif expect_type == "kata":
    #             value = str(value)

    #         else:
    #             # === auto detect ===
    #             if value.isdigit():
    #                 value = int(value)
    #             else:
    #                 try:
    #                     value = float(value)
    #                 except ValueError:
    #                     value = str(value)

    #         self.context[var_name] = value
    #         return value

    def call_function(self, func_name, args):

        # print(f"[DEBUG call_function] {func_name} args={args}")

        # fungsi masukkan()
        if func_name == "masukkan":
            return masukkan(self, args)

        # fungsi kataAcak()
        if func_name == "kataAcak":
            length = args[0] if args else 5
            return kataAcak(length)

        # fungsi angkaAcak()
        if func_name == "angkaAcak":
            if len(args) == 2:
                return angkaAcak(args[0], args[1])
            elif len(args) == 1:
                return angkaAcak(0, args[0])
            else:
                return angkaAcak()

        # fungsi UUID()
        if func_name == "UUID":
            return UUID()

        # fungsi tipedata
        if func_name == "tipedata":
            val = args[0]  # ambil argumen pertama
            return tipedata(val)

        # fungsi sandi()
        if func_name == "buatSandi":
            # args[0] di sini sudah berupa nilai (string/number) hasil evaluate_expr
            val = args[0] if args else ""
            # Pastikan selalu string di dalam buatSandi
            return buatSandi(str(val))

        if func_name == "cekSandi":
            # plain dan hashed sudah berupa nilai; jangan panggil evaluate_expr lagi
            if len(args) < 2:
                self.error("cekSandi butuh 2 argumen: (password_plain, hash_salt)")
                return False
            plain = args[0]
            hashed = args[1]
            # print(f"[DEBUG] cekSandi plain={repr(plain)} hashed={repr(hashed)}")
            result = cekSandi(plain, hashed)
            # print(f"[DEBUG] result={result}")
            return result
        
       # fungsi kelolaTxt()
        if func_name == "simpanTxt":
            return simpanTxt(
                args[0],              # filename
                args[1],              # content
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)  # path file .tarri
            )

        if func_name == "bacaTxt":
            key_arg = args[1] if len(args) > 1 else None
            result = bacaTxt(
                args[0],
                key=key_arg,
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)
            )
            # print(f"[DEBUG call_function] bacaTxt result={result}")
            return result

        if func_name == "perbaruiTxt":
            return perbaruiTxt(
                args[0],
                args[1],
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)
            )

        if func_name == "hapusTxt":
            return hapusTxt(
                args[0],
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)
            )



        # ========== JSON ==========
        if func_name == "simpanJson":
            return simpanJson(args[0], args[1]) if len(args) >= 2 else None

        if func_name == "bacaJson":
            return bacaJson(args[0]) if args else None

        if func_name == "perbaruiJson":
            return perbaruiJson(args[0], args[1]) if len(args) >= 2 else None

        if func_name == "hapusJson":
            return hapusJson(args[0]) if args else None


        if func_name not in self.functions:
            self.error(f"Fungsi '{func_name}' tidak ditemukan")
            return None
        params, body = self.functions[func_name]
        
        if len(args) != len(params):
            self.error(f"Jumlah argumen tidak cocok untuk fungsi '{func_name}'")
            return None

        saved_context = self.context.copy()
        saved_return = self._return_flag
        self._return_flag = None

        local_ctx = saved_context.copy()
        for p, a in zip(params, args):
            local_ctx[p] = a
            if self.status:
                print(f"[DEBUG] Argumen {p} = {a}")

        self.context = local_ctx

        for stmt in body.children:
            self.exec_node(stmt)
            if self._return_flag is not None:
                break

        result = self._return_flag
        self._return_flag = saved_return
        self.context = saved_context
        return result

    
    def exec_loop_stmt(self, node):
        # node typically: LOOP_VAR iterable block
        var_node = node.children[0]
        # var_node may be Token or Tree containing token
        if isinstance(var_node, Token):
            var_name = var_node.value
        elif isinstance(var_node, Tree) and var_node.children:
            first = var_node.children[0]
            var_name = first.value if isinstance(first, Token) else str(first)
        else:
            var_name = str(var_node)

        iterable = self.evaluate_expr(node.children[1])
        block = node.children[2]
        if iterable is None:
            self.error("Loop target bernilai null")
            return
        if not isinstance(iterable, list) and not hasattr(iterable, "__iter__"):
            self.error("Loop hanya bisa dijalankan pada list/iterable")
            return

        for item in iterable:
            if self._return_flag is not None:
                break
            # set loop variable in current context
            self.context[var_name] = item
            self.exec_node(block)

    # ======================
    # Evaluasi Ekspresi
    # ======================
    def evaluate_expr(self, node):
        if node is None:
            return None

        if isinstance(node, Tree):
            # param helper (rare in expression position)
            if node.data == "param" and node.children:
                child = node.children[0]
                return child.value if isinstance(child, Token) else str(child)

            # --- Perbaikan: tangani interpolasi pada node.data == "string" ---
            if node.data == "string":
                raw = node.children[0].value.strip('"')

                def replacer(match):
                    expr_code = match.group(1).strip()

                    # ===== CASE 1: ada indexing =====
                    if "[" in expr_code:
                        var_name, idx_expr = expr_code.split("[", 1)
                        var_name = var_name.strip()
                        idx_expr = idx_expr.rstrip("]").strip()

                        if "hingga" in idx_expr:
                            start, end = [s.strip() for s in idx_expr.split("hingga")]
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("slice_expr", [
                                    Token("NUMBER", start),
                                    Token("NUMBER", end),
                                ])
                            ])
                        elif "dan" in idx_expr:
                            first, second = [s.strip() for s in idx_expr.split("dan")]
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("pair_expr", [
                                    Token("NUMBER", first),
                                    Token("NUMBER", second),
                                ])
                            ])
                        else:
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("single_index", [Token("NUMBER", idx_expr)])
                            ])

                    # ===== CASE 2: cuma identifier biasa =====
                    else:
                        # biarkan evaluator lookup VAR_NAME -> kontekstual
                        sub_tree = Tree("identifier", [Token("VAR_NAME", expr_code)])

                    val = self.evaluate_expr(sub_tree)
                    return self.stringify(val, compact=True)

                text = re.sub(r"\{([^}]+)\}", replacer, raw)
                return DATATYPES["kata"](text)

            elif node.data == "number":
                val = node.children[0].value
                return DATATYPES["angka"](val) if val.isdigit() else DATATYPES["desimal"](val)

            elif node.data == "list_literal":
                return [self.evaluate_expr(ch) for ch in node.children]

            elif node.data == "add_expr":
                left = self.evaluate_expr(node.children[0])
                right = self.evaluate_expr(node.children[2])
                op = node.children[1].value
                if op == "+":
                    # biar aman, konversi campuran int+str ke str
                    if isinstance(left, str) or isinstance(right, str):
                        return str(left) + str(right)
                    return left + right
                elif op == "-":
                    return left - right

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

            elif node.data == "compare_expr":
                left = self.evaluate_expr(node.children[0])
                op = node.children[1].value
                right = self.evaluate_expr(node.children[2])
                return self.compare(op, left, right)

            elif node.data == "and_expr":
                return bool(self.evaluate_expr(node.children[0])) and bool(self.evaluate_expr(node.children[1]))

            elif node.data == "or_expr":
                return bool(self.evaluate_expr(node.children[0])) or bool(self.evaluate_expr(node.children[1]))

            elif node.data == "call_expr":
                # --- tangani type_cast ---
                if isinstance(node.children[0], Tree) and node.children[0].data == "type_cast":
                    cast_node = node.children[0]
                    inner_call = cast_node.children[0]  # call_expr asli
                    cast_type_token = cast_node.children[1]  # Token TYPE_CAST
                    cast_type = cast_type_token.value  # "angka" atau "kata"

                    # evaluasi inner call_expr
                    value = self.evaluate_expr(inner_call)

                    # lakukan casting
                    if cast_type == "angka":
                        try:
                            if "." in str(value):
                                value = float(value)
                            else:
                                value = int(value)
                        except ValueError:
                            # ambil nama variabel dengan aman
                            if len(inner_call.children) > 1:
                                args_node = inner_call.children[1]
                                if isinstance(args_node, Tree) and args_node.data == "args" and args_node.children:
                                    var_node = args_node.children[0]   # <-- ini ambil _usia
                                else:
                                    var_node = args_node
                            else:
                                var_node = None

                            if isinstance(var_node, Token):
                                var_name = var_node.value
                            elif isinstance(var_node, Tree) and var_node.data == "identifier":
                                first = var_node.children[0]
                                var_name = first.value if isinstance(first, Token) else str(first)
                            else:
                                var_name = str(var_node) if var_node else "?"

                            print()
                            print(f"[tarri] masukkan ({var_name}) hanya bisa menerima tipe data angka.")
                            return None


                    # simpan ke context
                    var_node = inner_call.children[0]
                    if isinstance(var_node, Token):
                        var_name = var_node.value
                    # elif isinstance(var_node, Tree) and var_node.data == "identifier":
                    #     first = var_node.children[0]
                    #     var_name = first.value if isinstance(first, Token) else str(first)
                    elif isinstance(node, Tree) and node.data == "identifier":
                        ident_token = node.children[0]
                        var_name = ident_token.value if isinstance(ident_token, Token) else str(ident_token)
                        return self.context.get(var_name, None)
                    else:
                        var_name = str(var_node) if var_node else "?"
                    self.context[var_name] = value
                    return value


                # --- normal call_expr seperti sebelumnya ---
                func_node = node.children[0]
                if isinstance(func_node, Token):
                    func_name = func_node.value
                elif isinstance(func_node, Tree) and func_node.data == "identifier" and func_node.children:
                    first = func_node.children[0]
                    func_name = first.value if isinstance(first, Token) else str(first)
                else:
                    func_name = str(func_node)

                # kumpulkan args
                args_values = []
                if len(node.children) > 1:
                    maybe_args = node.children[1]

                    if isinstance(maybe_args, Tree) and maybe_args.data == "args":
                        for i, a in enumerate(maybe_args.children):
                            if func_name == "masukkan" and i == 0:
                                # khusus masukkan: tetap simpan nama variabel mentah
                                args_values.append(a)
                            else:
                                val = self.evaluate_expr(a)
                                args_values.append(val)
                    else:
                        for i, a in enumerate(node.children[1:]):
                            if func_name == "masukkan" and i == 0:
                                args_values.append(a)
                            else:
                                args_values.append(self.evaluate_expr(a))

                return self.call_function(func_name, args_values)

            elif node.data == "identifier":
                name_token = node.children[0]
                name = name_token.value if isinstance(name_token, Token) else str(name_token)

                # === perbaikan utama ===
                if name in self.context:
                    return self.context[name]
                # kalau name tanpa _, coba dengan _
                if not name.startswith("_") and f"_{name}" in self.context:
                    return self.context[f"_{name}"]
                # kalau name pakai _, coba tanpa _
                if name.startswith("_") and name[1:] in self.context:
                    return self.context[name[1:]]

                # print(f"[DEBUG] identifier not found: {name}, ctx={self.context}")
                return None

            elif node.data == "indexing":
                obj_node = node.children[0]
                idx_node = node.children[1]

                # Ambil objek dari context
                if isinstance(obj_node, Token):
                    obj_name = obj_node.value
                    if obj_name not in self.context:
                        self.error(f"'{obj_name}' tidak ditemukan")
                        return None
                    obj = self.context[obj_name]
                else:
                    obj = self.evaluate_expr(obj_node)

                # Single index: obj[idx] atau obj[key]
                if idx_node.data == "single_index":
                    index_val = self.evaluate_expr(idx_node.children[0])
                    try:
                        if isinstance(obj, dict):
                            return obj.get(index_val)
                        else:
                            return obj[int(index_val)]
                    except (IndexError, KeyError, TypeError):
                        self.error(f"Index {index_val} di luar jangkauan untuk {obj_name}")
                        return None

                # Slice untuk list
                elif idx_node.data == "slice_expr":
                    start = self.evaluate_expr(idx_node.children[0])
                    end = self.evaluate_expr(idx_node.children[1])
                    try:
                        return obj[int(start):int(end)+1]
                    except Exception as e:
                        self.error(f"Slice gagal: {e}")
                        return None

                # Pair untuk list
                elif idx_node.data == "pair_expr":
                    try:
                        indices = [self.evaluate_expr(ch) for ch in idx_node.children]
                        return [obj[int(i)] for i in indices]
                    except Exception as e:
                        self.error(f"Pair gagal: {e}")
                        return None

                else:
                    self.error(f"Tidak tahu cara indexing dengan {idx_node.data}")
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
                        self.error(f"Nilai '{value}' tidak bisa dikonversi ke angka")
                        return None

                elif cast_type == "kata":
                    return str(value)

                else:
                    self.error(f"Tipe cast tidak dikenal: {cast_type}")
                    return value

            elif node.data == "true":
                return True
            elif node.data == "false":
                return False
            elif node.data == "null":
                return None

            # fallback: unknown tree type
            self.error(f"Tidak tahu cara evaluasi node jenis '{node.data}'")
            return None

        elif isinstance(node, Token):
            if node.type == "VAR_NAME":
                return self.context.get(node.value, None)
            elif node.type == "NUMBER":
                return DATATYPES["angka"](node.value) if node.value.isdigit() else DATATYPES["desimal"](node.value)
            elif node.type == "ESCAPED_STRING":
                raw = node.value.strip('"')

                def replacer(match):
                    expr_code = match.group(1).strip()

                    # ===== CASE 1: ada indexing =====
                    if "[" in expr_code:
                        var_name, idx_expr = expr_code.split("[", 1)
                        var_name = var_name.strip()
                        idx_expr = idx_expr.rstrip("]").strip()

                        if "hingga" in idx_expr:
                            start, end = [s.strip() for s in idx_expr.split("hingga")]
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("slice_expr", [
                                    Token("NUMBER", start),
                                    Token("NUMBER", end),
                                ])
                            ])
                        elif "dan" in idx_expr:
                            # Ambil semua indeks yang dipisahkan "dan"
                            parts = [s.strip() for s in idx_expr.split("dan")]
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("pair_expr", [Token("NUMBER", p) for p in parts])
                            ])
                        else:
                            sub_tree = Tree("indexing", [
                                Token("VAR_NAME", var_name),
                                Tree("single_index", [Token("NUMBER", idx_expr)])
                            ])

                    # ===== CASE 2: cuma identifier biasa =====
                    else:
                        sub_tree = Tree("identifier", [Token("VAR_NAME", expr_code)])

                    val = self.evaluate_expr(sub_tree)
                    return self.stringify(val, compact=True)

                text = re.sub(r"\{([^}]+)\}", replacer, raw)
                return DATATYPES["kata"](text)


            else:
                return node.value

        return None

    # ======================
    # Operator
    # ======================
    def compare(self, op, left, right):
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == "<": return left < right
        if op == ">": return left > right
        if op == "<=": return left <= right
        if op == ">=": return left >= right
        self.error(f"Operator perbandingan tidak dikenal: {op}")
        return False
        

    # def eval_atom(self, node):
    #     # === kalau Tree ===
    #     if isinstance(node, Tree):
    #         tag = node.data

    #         if tag == "number":
    #             v = node.children[0].value
    #             return float(v) if "." in v else int(v)

    #         elif tag == "string":
    #             raw = node.children[0].value
    #             return raw.strip('"').strip("'")

    #         elif tag == "true":     # literal 'benar'
    #             return True

    #         elif tag == "false":    # literal 'salah'
    #             return False

    #         elif tag == "null":     # literal 'kosong/hampa'
    #             return None

    #         elif tag == "identifier":
    #             v = node.children[0].value
    #             if v in self.env:
    #                 return self.env[v]
    #             else:
    #                 raise Exception(f"Identifier '{v}' tidak ditemukan")

    #         elif tag == "list_literal":
    #             return [self.eval_atom(child) for child in node.children]

    #         else:
    #             raise Exception(f"[tarri] Tidak tahu cara evaluasi node Tree jenis '{tag}'")

    #     # === kalau Token ===
    #     elif isinstance(node, Token):
    #         if node.type == "NUMBER":
    #             return float(node.value) if "." in node.value else int(node.value)

    #         elif node.type == "ESCAPED_STRING":
    #             return node.value.strip('"').strip("'")

    #         elif node.type in ("VAR_NAME", "NAME"):
    #             v = node.value
    #             if v in self.env:
    #                 return self.env[v]
    #             else:
    #                 raise Exception(f"Identifier '{v}' tidak ditemukan")

    #         else:
    #             return node.value  # fallback

    #     else:
    #         raise Exception(f"[tarri] Unknown atom node: {node}")



