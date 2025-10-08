# ==============================================================================#
# core.py - Interpreter Utama Tarri (TARRIAN)                                   #
# Bahasa TARRI versi 0.7.x                                                      #
# Teknologi Algoritmik Representasi Rekayasa Indonesia                          #
# ------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                          #
# Kontak  : danayasa2@gmail.com                                                 #
# Lisensi : MIT                                                                 #
# Situs   : bahasatarri.com                                                     #
# ------------------------------------------------------------------------------#
# Deskripsi :                                                                   #
# Inti interpreter Tarri untuk menjalankan skrip TARRI.                         #
# Dikembangkan dengan bantuan AI untuk memudahkan eksekusi dan pengembangan.    #
# Pengguna bebas memodifikasi dan meningkatkan fungsionalitas kode ini.         #
# ==============================================================================#

# Session (variabel global untuk menyimpan state)
from tarri.session.sesi import sesi as sesi_py
# Executor nodes (untuk mengeksekusi setiap tipe node AST)
from tarri.interpreter.exec_nodes.entry_point import exec_entry_point
from tarri.interpreter.exec_nodes.block import exec_block
from tarri.interpreter.exec_nodes.string import exec_string
from tarri.interpreter.exec_nodes.args import exec_args
from tarri.interpreter.exec_nodes.list_literal import exec_list_literal
from tarri.interpreter.exec_nodes.tabel_stmt import exec_tabel_stmt
from tarri.interpreter.exec_nodes.auto_var_decl import exec_auto_var_decl
from tarri.interpreter.exec_nodes.dict_literal import exec_dict_literal
from tarri.interpreter.exec_nodes.node import exec_node
from tarri.interpreter.exec_nodes.func_decl import exec_func_decl
from tarri.interpreter.exec_nodes.call_expr import exec_call_expr
from tarri.interpreter.exec_nodes.func_call import exec_func_call
from tarri.interpreter.exec_nodes.call_stmt import exec_call_stmt
from tarri.interpreter.exec_nodes.call_function import call_function
from tarri.interpreter.exec_nodes.evaluate_expr import evaluate_expr
from tarri.interpreter.exec_nodes.compare import compare
from tarri.interpreter.exec_nodes.foreach_stmt import exec_foreach_stmt
from tarri.interpreter.exec_nodes.loop_stmt import exec_loop_stmt, exec_break_stmt, exec_continue_stmt




class Context:
    
    def __init__(self, status=False, root_project=None):
        self.status = status
        self.functions = {}
        self._return_flag = None
        self.globals = {}
        self.context = self.globals
        
        self.context["sesi"] = sesi_py()  
        self.session = {}
        
        self.public_dir = None
        if root_project:
            self.public_dir = root_project
    
    def redirect(self, path, context):
        self.context["sesi"].simpan("redirect_data", context)
        return f"[REDIRECT]{path}"

    def error(self, msg):
        print(f"[tarri | interpreter] kesalahan : {msg}")

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

    def set_var(self, name, value):
            self.context[name] = value
            
    def get_var(self, name):
        if name in self.context:
            return self.context[name]
        elif name in self.globals:
            return self.globals[name]
        else:
            raise Exception(f"[tarri | interpreter] Variabel '{name}' tidak ditemukan")
     
    def exec_return_stmt(self, node):
        if node.children:
            self._return_flag = self.evaluate_expr(node.children[0])
        else:
            self._return_flag = None
        return self._return_flag
     
    def exec_print_stmt(self, node):
        expr_node = node.children[0]
        value = self.evaluate_expr(expr_node)
        
        if isinstance(value, bool):
            print("Benar" if value else "Salah")
        else:
            print(value)
            
    def exec_if_stmt(self, node):
        idx = 0

        # Eksekusi bagian "jika"
        if_branch = node.children[idx]
        kondisi_node = if_branch.children[0]
        block_node = if_branch.children[1]
        if self.evaluate_expr(kondisi_node):
            self.exec_node(block_node)
            return
        idx += 1

        # Eksekusi bagian "ataujika"
        while idx < len(node.children) - 1:
            kondisi_node = node.children[idx]
            block_node = node.children[idx + 1]
            if self.evaluate_expr(kondisi_node):
                self.exec_node(block_node)
                return
            idx += 2

        # Eksekusi bagian "lainnya" jika ada
        if idx < len(node.children):
            self.exec_node(node.children[idx])
     
    def evaluate_expr(self, node):
        from tarri.interpreter.exec_nodes.evaluate_expr import evaluate_expr as _eval
        return _eval(self, node)
    
    def exec_dict_literal(self, node):
        from tarri.interpreter.exec_nodes.dict_literal import exec_dict_literal as _dict_literal
        return _dict_literal(self, node)
    
    def exec_args(self, node):
        from tarri.interpreter.exec_nodes.args import exec_args as exec_args
        return exec_args(self, node)
    
    def call_function(self, func_name, args_values):
        from tarri.interpreter.exec_nodes.call_function import call_function as _call
        return _call(self, func_name, args_values)
    
    def exec_func_call(self, func_name, args_values):
        from tarri.interpreter.exec_nodes.func_call import exec_func_call as _exec
        return _exec(self, func_name, args_values)
    
    def compare(self, op, left, right):
        from tarri.interpreter.exec_nodes.compare import compare as _compare
        return _compare(self, op, left, right) 
      
    def exec_node(self, node):
        tipe = node.data

        if tipe == "start":
            for child in node.children:
                self.exec_node(child)

        elif tipe == "if_stmt":
            return self.exec_if_stmt(node)

        elif tipe == "print_stmt":
            return self.exec_print_stmt(node)

        elif tipe == "entry_point":
            return exec_entry_point(self, node)

        elif tipe == "block":
            return exec_block(self, node)

        elif tipe == "string":
            return exec_string(self, node)

        elif tipe == "args":
            return exec_args(self, node)

        elif tipe == "list_literal":
            return exec_list_literal(self, node)

        elif tipe == "tabel_stmt":
            return exec_tabel_stmt(self, node)

        elif tipe == "auto_var_decl":
            return exec_auto_var_decl(self, node)

        elif tipe == "dict_literal":
            return exec_dict_literal(self, node)

        elif tipe == "func_decl":
            return exec_func_decl(self, node)

        elif tipe == "call_expr":
            return exec_call_expr(self, node)

        elif tipe == "func_call":
            return exec_func_call(self, node)

        elif tipe == "call_stmt":
            return exec_call_stmt(self, node)

        elif tipe == "call_function":
            return call_function(self, node)

        elif tipe == "evaluate_expr":
            return evaluate_expr(self, node)

        elif tipe == "compare":
            return compare(self, node)

        elif tipe == "foreach_stmt":
            return exec_foreach_stmt(self, node)

        elif tipe == "loop_stmt":
            return exec_loop_stmt(self, node)

        elif tipe == "break_stmt":
            return exec_break_stmt(self, node)

        elif tipe == "continue_stmt":
            return exec_continue_stmt(self, node)

        elif tipe == "expr_stmt":
            return self.evaluate_expr(node.children[0])

        elif tipe == "return_stmt":
            if node.children:
                self._return_flag = self.evaluate_expr(node.children[0])
            else:
                self._return_flag = None
            return self._return_flag

        else:
            print(f"[tarri | interpreter] Node tidak dikenali: {tipe}")
            return None


    def run(self, ast):
        self._return_flag = None
        self.exec_node(ast)
        return self._return_flag
