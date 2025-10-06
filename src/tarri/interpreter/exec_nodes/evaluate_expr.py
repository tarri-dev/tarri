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
            
            elif node.data == "method_chain":
                obj = self.evaluate_expr(node.children[0])  # objek sebelumnya, misal sesi()
                method_name = node.children[1].value
                args = []
                if len(node.children) > 2:
                    args_node = node.children[2]
                    if args_node is not None:
                        args = [self.evaluate_expr(a) for a in args_node.children]
                if hasattr(obj, method_name):
                    return getattr(obj, method_name)(*args)
                else:
                    self.error(f"Objek tidak punya method '{method_name}'")
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

                        # tentukan tipe index
                        if (idx_expr.startswith('"') and idx_expr.endswith('"')) or (idx_expr.startswith("'") and idx_expr.endswith("'")):
                            key_token = Token("ESCAPED_STRING", idx_expr.strip("'\""))
                        elif idx_expr.isdigit():
                            key_token = Token("NUMBER", idx_expr)
                        else:
                            key_token = Token("VAR_NAME", idx_expr)

                        sub_tree = Tree("indexing", [
                            Token("VAR_NAME", var_name),
                            Tree("single_index", [key_token])
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

            elif node.data == "method_call_expr":
                # expr_atom "->" NAME "(" [args] ")"
                obj = self.evaluate_expr(node.children[0])  # objek, misal sesi()
                method_name = node.children[1].value        # nama method
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
                        raise Exception(f"Attribute '{method_name}' bukan method pada objek {type(obj)}")
                else:
                    raise Exception(f"Objek {type(obj)} tidak punya method '{method_name}'")

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

                        # tentukan tipe index
                        if (idx_expr.startswith('"') and idx_expr.endswith('"')) or (idx_expr.startswith("'") and idx_expr.endswith("'")):
                            key_token = Token("ESCAPED_STRING", idx_expr.strip("'\""))
                        elif idx_expr.isdigit():
                            key_token = Token("NUMBER", idx_expr)
                        else:
                            key_token = Token("VAR_NAME", idx_expr)

                        sub_tree = Tree("indexing", [
                            Token("VAR_NAME", var_name),
                            Tree("single_index", [key_token])
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