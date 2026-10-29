#==============================================================================#
# File    : list_literal.py                                                    #
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
#   'list_literal' dalam penerjemah Tarri.                                     #
#==============================================================================#

# tarri/interpreter/exec_nodes/exec_list_literal.py
# ==============================================================================#


def exec_list_literal(self, node):
    hasil = []
    for child in node.children:
        nilai = self.exec_node(child)
        hasil.append(nilai)
    return hasil
