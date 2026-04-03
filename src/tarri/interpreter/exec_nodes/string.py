#==============================================================================#
# File    : string.py                                                          #
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
#   'string' dalam penerjemah Tarri.                                           #
#==============================================================================#

# tarri/interpreter/exec_nodes/string.py
# ==============================================================================#
# string.py - fungsi utilitas untuk mengeksekusi atau “menyaring” string TARRI s
# sebagai kode mini.
# ==============================================================================#

# from tarri.interpreter.core import Context  # Optional, kalau perlu akses Context


def exec_string(self, node):
    value = node.children[0].value
    return value.strip('"')
