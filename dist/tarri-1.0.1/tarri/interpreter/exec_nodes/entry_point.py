#==============================================================================#
# File    : entry_point.py                                                     #
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
#   'entry_point' dalam penerjemah Tarri.                                      #
#==============================================================================#

# tarri/interpreter/exec_nodes/entry.py
# ==============================================================================#


def exec_entry_point(self, node):
    for stmt in node.children:
        self.exec_node(stmt)
