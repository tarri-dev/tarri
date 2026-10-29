#==============================================================================#
# File    : tabel_stmt.py                                                      #
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
#   'tabel_stmt' dalam penerjemah Tarri.                                       #
#==============================================================================#

# tarri/interpreter/exec_nodes/tabel_stmt.py
# ==============================================================================#

from lark import Tree


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
        self.error(
            f"[tarri | interpreter | tabel_stmt] Objek tidak memiliki metode '{method_name}'"
        )
        return None
