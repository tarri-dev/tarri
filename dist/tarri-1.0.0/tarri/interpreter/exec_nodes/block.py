#==============================================================================#
# File    : block.py                                                           #
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
#   'block' dalam penerjemah Tarri.                                            #
#==============================================================================#

# tarri/interpreter/exec_nodes/block.py
# ==============================================================================#
# block.py - menangani blok kode (block) → biasanya { ... }
# atau satu grup statement dalam fungsi, loop, atau conditional.
# ==============================================================================#

# from tarri.interpreter.core import Context  # Optional, kalau perlu akses Context

from collections import ChainMap


def exec_block(self, node, new_scope=True):
    """Eksekusi blok kode { ... }.

    Args:
        new_scope: Jika True (default), buat scope lokal baru (untuk fungsi & if).
                   Jika False, jalankan langsung di scope saat ini (untuk loop body).
    """
    if new_scope:
        local_env = {}
        saved_context = self.context
        self.context = ChainMap(local_env, self.context)
    else:
        saved_context = None

    try:
        result = None
        for stmt in node.children:
            if self._return_flag is not None:
                break
            val = self.exec_node(stmt)
            if self._return_flag is not None:
                result = val
                break
        return result
    finally:
        if new_scope:
            self.context = saved_context
