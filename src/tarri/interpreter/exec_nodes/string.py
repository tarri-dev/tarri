# tarri/interpreter/exec_nodes/string.py
# ==============================================================================#
# string.py - fungsi utilitas untuk mengeksekusi atau “menyaring” string TARRI s
# sebagai kode mini.
# ==============================================================================#

# from tarri.interpreter.core import Context  # Optional, kalau perlu akses Context


def exec_string(self, node):
        value = node.children[0].value
        return value.strip('"')