#==============================================================================#
# File    : foreach_stmt.py                                                    #
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
#   'foreach_stmt' dalam penerjemah Tarri.                                     #
#==============================================================================#

# def exec_foreach_stmt(self, node):
#     var_name = node.children[0].value
#     iterable = self.evaluate_expr(node.children[1])
#     for item in iterable:
#         self._ctx[var_name] = item
#         self.exec_block(node.children[2])


def exec_foreach_stmt(self, node):

    print("exec foreach terpanggil")
    var_name = node.children[0].value
    iterable = self.evaluate_expr(node.children[1])

    # backup flag
    old_flag = getattr(self, "in_loop", False)
    self.in_loop = True

    try:
        for item in iterable:
            self.context[var_name] = item
            self.exec_block(node.children[2])
    finally:
        # restore
        self.in_loop = old_flag
