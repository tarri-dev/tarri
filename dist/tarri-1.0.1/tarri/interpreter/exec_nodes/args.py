#==============================================================================#
# File    : args.py                                                            #
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
#   'args' dalam penerjemah Tarri.                                             #
#==============================================================================#

# tarri/interpreter/exec_nodes/args.py
# ==============================================================================#


def exec_args(self, node):
    return [self.exec_node(child) for child in node.children]
