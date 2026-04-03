# ==============================================================================#
# core.py - Interpreter Utama Tarri (TARRIAN)                                   #
# Bahasa TARRI versi 0.8.x                                                      #
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


# Executor nodes (untuk mengeksekusi setiap tipe node AST)
from tarri.interpreter.exec_nodes.entry_point import exec_entry_point
from tarri.interpreter.exec_nodes.block import exec_block
from tarri.interpreter.exec_nodes.string import exec_string
from tarri.interpreter.exec_nodes.args import exec_args
from tarri.interpreter.exec_nodes.list_literal import exec_list_literal
from tarri.interpreter.exec_nodes.tabel_stmt import exec_tabel_stmt
from tarri.interpreter.exec_nodes.auto_var_decl import exec_auto_var_decl
from tarri.interpreter.exec_nodes.index_assign import exec_index_assign
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
from tarri.interpreter.exec_nodes.loop_stmt import (
    exec_loop_stmt,
    exec_break_stmt,
    exec_continue_stmt,
)
from tarri.errors import BreakSignal, ContinueSignal, TarriRuntimeError
import re
from collections import ChainMap
from lark import Tree, Token
from tarri.session.sesi import SesiManager


class Context:

    # Menggunakan sinyal dari errors.py (single source of truth)
    BreakSignal = BreakSignal
    ContinueSignal = ContinueSignal

    def error(self, msg):
        from tarri.errors import TarriRuntimeError

        raise TarriRuntimeError(msg)

    # Tambahkan ini di kelas Context (core.py)
    def call_method(self, obj, method_name, args_values):
        from tarri.interpreter.exec_nodes.call_function import (
            call_method as _call_method,
        )

        # Pastikan Anda mempassing 'self' (konteks interpreter)
        return _call_method(self, obj, method_name, args_values)

    def __init__(
        self,
        status=False,
        root_project=None,
        sesi: SesiManager = None,
        browser_sesi_id=None,
    ):
        self.status = status
        self.public_dir = root_project if root_project else None

        # --- PERBAIKAN: Gunakan factory dict() untuk memastikan isolation ---
        self.globals = dict()
        self.context_stack = [self.globals]
        self.context = self.globals

        # Fungsi runtime
        self.functions = dict()

        # Sesi harus benar-benar unik per instance
        if sesi is not None:
            self.session = sesi
        else:
            # Jika browser_sesi_id None, SesiManager harus buat ID baru, bukan ambil yang terakhir
            self.session = SesiManager(sesi_id=browser_sesi_id)

        self.globals["sesi"] = self.session

        # Pastikan NIL_VALUE unik per instance agar tidak terjadi tabrakan pembandingan
        self.NIL_VALUE = object()
        # Sentinel khusus untuk 'sembunyikan' (void return - return tanpa nilai)
        self._VOID_RETURN = object()
        self._return_flag = None
        self.in_loop = False

    def translate_to_python(self, tarri_value):
        """
        Mengubah nilai internal Tarri menjadi tipe data Python primitif
        untuk digunakan oleh fungsi FFI (extension Python).
        """
        # 1. Nilai Null/NIL
        if tarri_value is self.NIL_VALUE or tarri_value is None:
            return None

        # 2. Tipe Primitif Python yang sudah kompatibel (untuk mencegah re-wrapping)
        if isinstance(tarri_value, (bool, dict, list, str, int, float)):
            return tarri_value

        # 3. Asumsi Tarri menggunakan kelas pembungkus untuk data (String, Number)
        # Anda perlu mengganti 'TarriStringType' dan 'TarriNumberType'
        # dengan kelas atau tipe data Tarri Anda yang sebenarnya.

        # CONTOH: Jika nilai TarriString memiliki atribut '.value'
        if hasattr(tarri_value, "value"):
            return tarri_value.value

        # CONTOH: Jika nilai Tarri adalah objek FFI (misal: SQLiteHandler)
        # Ini harus dikembalikan apa adanya agar bisa dipanggil metodenya.
        return tarri_value

    def eval_arg(self, a):
        # --------------------------------------
        # Node Tree
        # --------------------------------------
        if isinstance(a, Tree):
            if a.data == "call_expr":
                return self.evaluate_expr(a)

            elif a.data == "string":
                # Menghapus str() di sini karena string dievaluasi sebagai nilai literal
                return a.children[0].value

            elif a.data == "identifier":
                # PERUBAHAN: Gunakan get_var() untuk scoping yang benar
                first = a.children[0]
                return self.get_var(first.value)

            elif a.data == "slice_expr":  # Asumsi parser mendukung slice_expr
                var_name = a.children[0].value
                start = self.evaluate_expr(a.children[1])
                end = self.evaluate_expr(a.children[2])
                seq = self.get_var(var_name)
                return seq[int(start) : int(end)]

            else:
                # Gabungan string atau node yang tidak dikenali
                values = [str(self.eval_arg(c)) for c in a.children]
                joined = " ".join(values)

                # PERUBAHAN: Menghapus logika regex slice dari sini (seharusnya di parser/slice_expr)
                return joined

        # --------------------------------------
        # Token
        # --------------------------------------
        elif isinstance(a, Token):
            if a.type == "VAR_NAME":
                # PERUBAHAN: Gunakan get_var() untuk scoping yang benar
                return self.get_var(a.value)

            # elif a.type == "HTML_BLOCK":
            #     return a.value

            elif a.type == "TRUE":
                return True
            elif a.type == "FALSE":
                return False
            elif a.type == "NUMBER":
                try:
                    return int(a.value)
                except ValueError:
                    return float(a.value)
            else:
                return a.value

        # --------------------------------------
        # Literal / lainnya
        # --------------------------------------
        elif isinstance(a, str):
            # PERUBAHAN: Menghapus logika regex slice dari sini
            return a
        else:
            return a

    def _context_as_str_dict(self):
        return {
            k: (str(v) if v is not None else "null") for k, v in self.context.items()
        }

    def stringify(self, value, compact=False):
        if value is None:
            return "null"
        # ... (Logika stringify lainnya tetap sama) ...
        if isinstance(value, list):
            if compact:
                return ", ".join(self.stringify(v, compact=True) for v in value)
            else:
                return "[ " + ", ".join(self.stringify(v) for v in value) + " ]"

        # PERBAIKAN: Handle Boolean Tarri
        if isinstance(value, bool):
            return "Benar" if value else "Salah"

        return str(value)

    def set_var(self, name, value, node=None):
        # 1. Jika context adalah ChainMap, cari di mana variabel berada
        if isinstance(self.context, ChainMap):
            for mapping in self.context.maps:
                if name in mapping:
                    mapping[name] = value
                    return
            # Jika tidak ditemukan, masukkan ke scope lokal (map pertama)
            self.context[name] = value
            return

        # 2. Jika context adalah dict biasa (global scope)
        self.context[name] = value

    def get_var(self, name, node=None):
        # Ambil dari context (ChainMap atau dict akan mencari secara hierarkis)
        if name in self.context:
            return self.context[name]

        # Jika variabel tidak ditemukan
        line = None
        if node:
            if hasattr(node, "line"):
                line = node.line
            elif hasattr(node, "meta") and hasattr(node.meta, "line"):
                line = node.meta.line

        from tarri.errors import VariabelTidakDitemukan

        raise VariabelTidakDitemukan(name, baris=line)

    def exec_return_stmt(self, node):
        if node.children:
            val = self.evaluate_expr(node.children[0])

            if isinstance(val, str) and "<" in val:
                import re

                def replace_variable(match):
                    var_name = match.group(1).strip()
                    try:
                        result = self.get_var(var_name)
                        return str(result) if result is not None else ""
                    except Exception:
                        return match.group(0)

                val = re.sub(r"\{+\s*(.*?)\s*\}+", replace_variable, val)

            self._return_flag = val
        else:
            # sembunyikan / return tanpa nilai → flag dengan sentinel agar
            # exec_func_call tahu bahwa return sudah dipanggil (tapi nilainya None)
            self._return_flag = self._VOID_RETURN

    def exec_print_stmt(self, node):
        outputs = []

        for child in node.children:
            value = self.evaluate_expr(child)
            # PERUBAHAN: Penghapusan penanganan Boolean di sini
            outputs.append(
                self.stringify(value) if value is not None else ""
            )  # Gunakan stringify

        print(" ".join(outputs), flush=True)

    def exec_if_stmt(self, node):
        idx = 0

        # Eksekusi bagian "jika"
        if_branch = node.children[idx]
        kondisi_node = if_branch.children[0]
        block_node = if_branch.children[1]

        # Menggunakan Python truthiness: None, 0, False, string kosong = False
        if bool(self.evaluate_expr(kondisi_node)):
            self.exec_node(block_node)
            return
        idx += 1

        # Eksekusi bagian "ataujika"
        while idx < len(node.children) - 1:
            kondisi_node = node.children[idx]
            block_node = node.children[idx + 1]
            if bool(self.evaluate_expr(kondisi_node)):
                self.exec_node(block_node)
                return
            idx += 2

        # Eksekusi bagian "lainnya" jika ada
        if idx < len(node.children) and node.children[idx].data == "block":
            self.exec_node(node.children[idx])

    # --- Delegasi Method Tambahan --- (Dipertahankan)
    def evaluate_expr(self, node):
        from tarri.interpreter.exec_nodes.evaluate_expr import evaluate_expr as _eval

        return _eval(self, node)

    def exec_dict_literal(self, node):
        from tarri.interpreter.exec_nodes.dict_literal import (
            exec_dict_literal as _dict_literal,
        )

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

        # --- Tambahkan penanganan sinyal Break/Continue ---
        if tipe == "break_stmt":
            raise self.BreakSignal()
        elif tipe == "continue_stmt":
            raise self.ContinueSignal()

        if tipe == "start":
            for child in node.children:
                try:
                    self.exec_node(child)
                    if self._return_flag is not None:
                        break
                except StopIteration:
                    raise
                except TarriRuntimeError:
                    raise

        # --- Penanganan node yang didelegasikan atau di-refactor ---
        elif tipe == "if_stmt":
            return self.exec_if_stmt(node)

        elif tipe == "print_stmt":
            return self.exec_print_stmt(node)

        elif tipe == "entry_point":
            return exec_entry_point(self, node)

        elif tipe == "block":
            # Perhatikan: exec_block HARUS menangani return dan context stack (pop/push)
            return exec_block(self, node)

        elif tipe == "return_stmt":
            # Panggil exec_return_stmt, yang hanya mengatur flag
            self.exec_return_stmt(node)

        elif tipe == "expr_stmt":
            self.evaluate_expr(node.children[0])

        elif tipe == "try_catch_stmt":
            coba_block = node.children[0]
            var_name_token = (
                node.children[1]
                if len(node.children) > 1 and node.children[1] is not None
                else None
            )
            var_name = (
                var_name_token.value
                if var_name_token and isinstance(var_name_token, Token)
                else None
            )
            tangkap_block = (
                node.children[2]
                if len(node.children) > 2 and node.children[2] is not None
                else None
            )
            akhirnya_block = (
                node.children[3]
                if len(node.children) > 3 and node.children[3] is not None
                else None
            )

            try:
                exec_block(self, coba_block, new_scope=False)
            except TarriRuntimeError as e:
                if tangkap_block:
                    if var_name:
                        msg = str(e)
                        self.set_var(var_name, msg)
                    exec_block(self, tangkap_block, new_scope=False)
            except Exception as e:
                if tangkap_block:
                    if var_name:
                        msg = str(e)
                        self.set_var(var_name, msg)
                    exec_block(self, tangkap_block, new_scope=False)
            finally:
                if akhirnya_block:
                    exec_block(self, akhirnya_block, new_scope=False)
        # --- Node Delegasi (tetap sama) ---
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
        elif tipe == "index_assign":
            return exec_index_assign(self, node)
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
        elif tipe == "null_coalesce":
            return evaluate_expr(self, node)
        # break/continue now handled by exception raising at top of exec_node
        elif tipe in ["break_stmt", "continue_stmt"]:
            pass
        # -----------------------------------

        else:
            self.error(f"Node tidak dikenali: {tipe}")
            return None

    def run(self, ast):
        self._return_flag = None

        # 1. Daftarkan semua fungsi terlebih dahulu
        if isinstance(ast, Tree) and ast.data == "start":
            for node in ast.children:
                if isinstance(node, Tree) and node.data == "func_decl":
                    try:
                        exec_func_decl(self, node)
                    except Exception as e:
                        self.error(f"Gagal memuat fungsi: {e}")

        # 2. Jalankan eksekusi
        try:
            self.exec_node(ast)

        except StopIteration as stop:
            raise stop
        except TarriRuntimeError as e:
            raise e

        return self._return_flag
