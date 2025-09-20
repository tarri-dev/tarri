from lark import Tree, Token
from tarri.keywords import KEYWORDS
import tarri.keyword_list
from tarri.datatypes import DATATYPES
import tarri.datatypes_list
import re
from collections import ChainMap

from tarri.functions.kataAcak import kataAcak
from tarri.functions.angkaAcak import angkaAcak
from tarri.functions.uuid import UUID
from tarri.functions.tipedata import tipedata
from tarri.functions.masukkan import masukkan
from tarri.functions.lacak import lacak
from tarri.functions.sandi import buatSandi, cekSandi
from tarri.functions.kelolaTxt import simpanTxt, bacaTxt, perbaruiTxt, hapusTxt
# from tarri.functions.kelolaJson import simpanJson, bacaJson, perbaruiJson, hapusJson


# import blueprint baru
from tarri.database.buatbasisdata import BuatBasisData
from tarri.database.buattabel import BasisData, BuatTabel, HapusTabel
from tarri.database.permintaan import simpan,ambil,semua,rapi,dimana,atau_dimana,ubah,hapus,dan_dimana





class Interpreter:
    def __init__(self, status=False):
        self.status = status
        self.functions = {}
        self._return_flag = None
        self.globals = {}
        self.context = self.globals  # default context mengarah ke globals

    def error(self, msg):
        print(f"[tarri] kesalahan : {msg}")

    def _context_as_str_dict(self):
        return {k: (str(v) if v is not None else "null") for k, v in self.context.items()}

    def stringify(self, value, compact=False):
        if value is None:
            return "null"
        if isinstance(value, list):
            if compact:
                return ", ".join(self.stringify(v, compact=True) for v in value)
            else:
                return "[ " + ", ".join(self.stringify(v) for v in value) + " ]"
        return str(value)

    def run(self, tree):
        for stmt in tree.children:
            self.exec_node(stmt)

    def exec_entry_point(self, node):
        for stmt in node.children:
            self.exec_node(stmt)

    def exec_block(self, node):
        result = None
        for stmt in node.children:
            if self._return_flag is not None:
                break
            val = self.exec_node(stmt)
            if self._return_flag is not None:
                result = val
                break
        return result

    def exec_string(self, node):
        value = node.children[0].value
        return value.strip('"')

    def exec_args(self, node):
        return [self.exec_node(child) for child in node.children]

    def exec_list_literal(self, node):
        hasil = []
        for child in node.children:
            nilai = self.exec_node(child)
            hasil.append(nilai)
        return hasil

    def exec_tabel_stmt(self, node):
        target_var = node.children[0].value
        target = self.context.get(target_var)
        method_node = node.children[1]
        method_name = method_node.children[0].value
        args = []

        if len(method_node.children) > 1:
            for child in method_node.children[1:]:
                if isinstance(child, Tree) and child.data == "args":
                    args = self.exec_args(child)
                else:
                    args.append(self.exec_node(child))

        if hasattr(target, method_name):
            func = getattr(target, method_name)
            func(*args)  # panggil method tapi jangan assign ke target
            return target  # selalu return objek asli
        else:
            self.error(f"Builder tidak punya method '{method_name}'")
            return None



    def exec_auto_var_decl(self, node):
        var_name = node.children[0].value
        value_node = node.children[2] if len(node.children) > 2 else None
        value = self.evaluate_expr(value_node) if value_node is not None else None
        self.context[var_name] = value
        if self.status:
            print(f"[DEBUG] Assigned {var_name} = {value}")
        return value

    def exec_node(self, node):
        if not isinstance(node, Tree):
            return None
        if node.data in KEYWORDS:
            handler = KEYWORDS[node.data]
            return handler(self, node.children)
        handler_name = f"exec_{node.data}"
        if hasattr(self, handler_name):
            return getattr(self, handler_name)(node)
        if node.data == "list_literal":
            return self.exec_list_literal(node)
        # expr_stmt fallback: jika grammar menghasilkan expr_stmt tapi tidak ada handler
        if node.data == "expr_stmt":
            # child is an expr tree — evaluate it
            return self.evaluate_expr(node.children[0]) if node.children else None
        self.error(f"Tidak tahu cara eksekusi {node.data}")
        return None

    def exec_func_decl(self, node):
        func_name = node.children[0].value
        params_node = node.children[1] if len(node.children) > 1 else None
        params = []
        if isinstance(params_node, Tree) and params_node.data == "params":
            for p in params_node.children:
                if isinstance(p, Tree) and p.data == "param" and p.children:
                    child = p.children[0]
                    params.append(child.value if isinstance(child, Token) else str(child))
                elif isinstance(p, Token):
                    params.append(p.value)
        body = node.children[-1]
        self.functions[func_name] = (params, body)
        if self.status:
            print(f"[DEBUG] Fungsi '{func_name}' terdaftar dengan parameter {params}")
        return None

    def exec_call_expr(self, node):
        func_name_node = node.children[0]
        func_name = func_name_node.value if isinstance(func_name_node, Token) else str(func_name_node)

        args_node = node.children[1] if len(node.children) > 1 else None
        args = []
        if args_node:
            for i, arg in enumerate(args_node.children):
                if func_name == "masukkan" and i == 0:
                    args.append(arg)
                else:
                    args.append(self.evaluate_expr(arg))

        result = self.exec_func_call(func_name, args)
        return result


    def exec_func_call(self, func_name, args):
        if func_name not in self.functions:
            self.error(f"Fungsi '{func_name}' tidak ditemukan")
            return None
        params, body = self.functions[func_name]
        local_env = {}
        for i, param in enumerate(params):
            local_env[param] = args[i] if i < len(args) else None
            if self.status:
                print(f"[DEBUG] Argumen {param} = {local_env[param]}")
        saved_context = self.context
        saved_return = self._return_flag
        self._return_flag = None
        try:
            self.context = ChainMap(local_env, self.globals)
            result = None
            for stmt in body.children:
                self.exec_node(stmt)
                if self._return_flag is not None:
                    result = self._return_flag
                    break
            return result
        finally:
            self._return_flag = saved_return
            self.context = saved_context

    def set_var(self, name, value):
        self.context[name] = value

    def get_var(self, name):
        if name in self.context:
            return self.context[name]
        elif name in self.globals:
            return self.globals[name]
        else:
            raise Exception(f"Variabel '{name}' tidak ditemukan")

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

    def call_function(self, func_name, args):
                    
        if func_name in ("simpan","ambil","semua","dimana","rapi","atau_dimana","dan_dimana","ubah","hapus"):
            try:
                if func_name == "simpan":
                    hasil = simpan(*args)
                    return hasil
                
                if func_name == "ambil":
                    try:
                        # args = [bd_lokasi, bd_nama, tabel_nama, method, ...]
                        bd_lokasi  = args[0]
                        bd_nama    = args[1]
                        tabel_nama = args[2]
                        method     = args[3] if len(args) > 3 else "semua"
                        extra_args = args[4:]

                        # inisialisasi objek aktif
                        ambil(bd_lokasi, bd_nama, tabel_nama)

                        # jalankan sesuai method
                        if method == "semua":
                            hasil = semua()
                        elif method == "dimana":
                            if len(extra_args) >= 2:
                                kolom, nilai = extra_args[0], extra_args[1]
                                dimana(kolom, nilai)
                                hasil = semua()
                            else:
                                hasil = "gagal: kurang argumen untuk 'dimana'"
                        elif method == "atau_dimana":
                            if len(extra_args) >= 2:
                                kolom, nilai = extra_args[0], extra_args[1]
                                atau_dimana(kolom, nilai)
                                hasil = semua()
                            else:
                                hasil = "gagal: kurang argumen untuk 'atau_dimana'"
                                
                        elif method == "dan_dimana":
                            if len(extra_args) >= 2:
                                kolom, nilai = extra_args[0], extra_args[1]
                                dan_dimana(kolom, nilai)
                                hasil = semua()
                            else:
                                hasil = "gagal: kurang argumen untuk 'dan_dimana'"

                        else:
                            hasil = "gagal: method tidak dikenali"

                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"

                    return hasil
                
                if func_name == "ubah":
                    try:
                        bd_lokasi  = args[0]
                        bd_nama    = args[1]
                        tabel_nama = args[2]
                        data_baru  = args[3] if len(args) > 3 else {}

                        ubah(bd_lokasi, bd_nama, tabel_nama, data_baru)

                        if len(args) >= 6 and args[4] == "dimana":
                            kolom, nilai = args[5], args[6]
                            hasil = dimana(kolom, nilai)
                        else:
                            hasil = "gagal: ubah perlu 'dimana'"
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"

                    return hasil


                if func_name == "hapus":
                    try:
                        bd_lokasi  = args[0]
                        bd_nama    = args[1]
                        tabel_nama = args[2]
                        dummy_data = args[3] if len(args) > 3 else None

                        hapus(bd_lokasi, bd_nama, tabel_nama, dummy_data)

                        if len(args) >= 5 and args[4] == "dimana":
                            kolom, nilai = args[5], args[6]
                            hasil = dimana(kolom, nilai)
                        else:
                            hasil = "gagal: hapus perlu 'dimana'"
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"

                    return hasil
                
                if func_name == "semua":
                    try:
                        hasil = semua()
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"
                    return hasil

                if func_name == "dimana":
                    try:
                        kolom = args[0]
                        nilai = args[1]
                        hasil = dimana(kolom, nilai)
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"
                    return hasil

                if func_name == "atau_dimana":
                    try:
                        kolom = args[0]
                        nilai = args[1]
                        hasil = atau_dimana(kolom, nilai)
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"
                    return hasil
                
                if func_name == "dan_dimana":
                    try:
                        kolom = args[0]
                        nilai = args[1]
                        hasil = dan_dimana(kolom, nilai)
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"
                    return hasil
                
                if func_name == "rapi":
                    try:
                        hasil = rapi(*args)
                    except Exception as e:
                        print(f"[tarri] kesalahan : {e}")
                        hasil = "gagal"
                    return hasil


            except Exception as e:
                self.error(f"[ERROR {func_name}] {e}")
                return "gagal"
                    

        
        if func_name == "masukkan":
            return masukkan(self, args)
        
        if func_name == "lacak":
            return lacak(self, args)
        
        if func_name == "BuatBasisData":
            hasil, pesan = BuatBasisData(*args)
            self.context["i"] = pesan

            # inject context ke modul buattabel
            try:
                from tarri.database import buattabel
                buattabel.set_db_context(self.context)
            except Exception as e:
                print(f"[WARN] gagal inject context ke buattabel: {e}")
            return hasil

        
        if func_name == "BasisData":
            return BasisData()

        if func_name == "BuatTabel":
            if len(args) < 1:
                self.error("BuatTabel butuh 1 argumen: (bd_obj)")
                return "gagal"
            hasil, pesan = BuatTabel(args[0])
            self.context["i"] = pesan
            return hasil

        if func_name == "HapusTabel":
            # Bisa dipanggil dengan 2 atau 3 argumen
            if len(args) == 2:
                nama_db, nama_tabel = args
                hasil = HapusTabel(nama_db, nama_tabel)
                return hasil
            elif len(args) == 3:
                nama_db, nama_tabel, lokasi_db = args
                hasil = HapusTabel(nama_db, nama_tabel, lokasi_db)
                return hasil
            else:
                return "gagal"



        if func_name == "kataAcak":
            length = args[0] if args else 5
            return kataAcak(length)
        
        if func_name == "angkaAcak":
            if len(args) == 2:
                return angkaAcak(args[0], args[1])
            elif len(args) == 1:
                return angkaAcak(0, args[0])
            else:
                return angkaAcak()
            
        if func_name == "UUID":
            return UUID()
        
        if func_name == "tipedata":
            val = args[0]
            return tipedata(val)
        
        if func_name == "buatSandi":
            val = args[0] if args else ""
            return buatSandi(str(val))
            
        if func_name == "cekSandi":
            if len(args) < 2:
                self.error("cekSandi butuh 2 argumen: (password_plain, hash_salt)")
                return False
            plain = args[0]
            hashed = args[1]
            result = cekSandi(plain, hashed)
            return result
        
        if func_name == "simpanTxt":
            return simpanTxt(
                args[0],
                args[1],
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)
            )
            
        if func_name == "bacaTxt":
            key_arg = args[1] if len(args) > 1 else None
            result = bacaTxt(
                args[0],
                key=key_arg,
                ctx=self.context,
                tarri_file=getattr(self, "current_file", None)
            )
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

        if func_name in self.functions:
            return self.exec_func_call(func_name, args)

        self.error(f"Fungsi '{func_name}' tidak ditemukan")
        return None

    def exec_loop_stmt(self, node):
        var_node = node.children[0]
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
            self.context[var_name] = item
            self.exec_node(block)

    def evaluate_expr(self, node):
        if node is None:
            return None
        if isinstance(node, Tree):
            if node.data == "param" and node.children:
                child = node.children[0]
                return child.value if isinstance(child, Token) else str(child)
            
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
                        raise Exception(f"Tipe cast '{cast_type}' tidak dikenal")
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
                if isinstance(node.children[0], Tree) and node.children[0].data == "type_cast":
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
                elif isinstance(func_node, Tree) and func_node.data == "identifier" and func_node.children:
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

            elif node.data == "string":
                raw = node.children[0].value.strip('"')
                def replacer(match):
                    expr_code = match.group(1).strip()
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
                    else:
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

            elif node.data == "identifier":
                name_token = node.children[0]
                name = name_token.value if isinstance(name_token, Token) else str(name_token)
                if name in self.context:
                    return self.context[name]
                if not name.startswith("_") and f"_{name}" in self.context:
                    return self.context[f"_{name}"]
                if name.startswith("_") and name[1:] in self.context:
                    return self.context[name[1:]]
                return None

            elif node.data == "indexing":
                obj_node = node.children[0]
                idx_node = node.children[1]
                if isinstance(obj_node, Token):
                    obj_name = obj_node.value
                    if obj_name not in self.context:
                        self.error(f"'{obj_name}' tidak ditemukan")
                        return None
                    obj = self.context[obj_name]
                else:
                    obj = self.evaluate_expr(obj_node)
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
                elif idx_node.data == "slice_expr":
                    start = self.evaluate_expr(idx_node.children[0])
                    end = self.evaluate_expr(idx_node.children[1])
                    try:
                        return obj[int(start):int(end)+1]
                    except Exception as e:
                        self.error(f"Slice gagal: {e}")
                        return None
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
                    else:
                        sub_tree = Tree("identifier", [Token("VAR_NAME", expr_code)])
                    val = self.evaluate_expr(sub_tree)
                    return self.stringify(val, compact=True)
                text = re.sub(r"\{([^}]+)\}", replacer, raw)
                return DATATYPES["kata"](text)
            else:
                return node.value
        return None

    def compare(self, op, left, right):
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == "<": return left < right
        if op == ">": return left > right
        if op == "<=": return left <= right
        if op == ">=": return left >= right
        self.error(f"Operator perbandingan tidak dikenal: {op}")
        return False
