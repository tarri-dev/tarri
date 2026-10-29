#==============================================================================#
# File    : dict_literal.py                                                    #
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
#   'dict_literal' dalam penerjemah Tarri.                                     #
#==============================================================================#

# tarri/interpreter/exec_nodes/dict_literal.py
# ==============================================================================#


def exec_dict_literal(self, node):
    value = {}
    for pair in node.children:
        key_node = pair.children[0]
        val_node = pair.children[1]

        # ambil key
        if key_node.type == "ESCAPED_STRING":
            key = key_node.value.strip('"')
        else:
            key = key_node.value  # VAR_NAME atau NAME

        # evaluasi value
        val = self.evaluate_expr(val_node)
        value[key] = val

    return value
