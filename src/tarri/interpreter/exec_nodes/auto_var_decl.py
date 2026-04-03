#==============================================================================#
# File    : auto_var_decl.py                                                   #
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
#   'auto_var_decl' dalam penerjemah Tarri.                                    #
#==============================================================================#

# tarri/interpreter/exec_nodes/auto_var_decl.py
# ==============================================================================#


def exec_auto_var_decl(self, node):
    var_name = node.children[0].value
    op_node = node.children[1] if len(node.children) > 1 else None
    value_node = node.children[2] if len(node.children) > 2 else None
    value = self.evaluate_expr(value_node) if value_node is not None else None

    if op_node.type == "EQUAL":
        self.set_var(var_name, value)
    elif op_node.type == "PLUS_EQUAL":
        old = self.get_var(var_name)
        if isinstance(value, list):
            self.set_var(var_name, old + value)
        else:
            self.set_var(var_name, old + value)
    elif op_node.type == "MINUS_EQUAL":
        old = self.get_var(var_name)
        self.set_var(var_name, old - value)
    else:
        self.error(
            f"[tarri | interpreter | auto_var_decl] Operator penugasan tidak dikenal: {op_node.value}"
        )
