#==============================================================================#
# File    : index_assign.py                                                    #
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
#   'index_assign' dalam penerjemah Tarri.                                     #
#==============================================================================#

# tarri/interpreter/exec_nodes/index_assign.py


def exec_index_assign(self, node):
    var_name = node.children[0].value
    idx_node = node.children[1]
    op_node = node.children[2]
    val_node = node.children[3]

    val = self.evaluate_expr(val_node)

    obj = self.get_var(var_name)
    if obj is None:
        self.error(f"Variabel/List/Kamus '{var_name}' tidak ditemukan")
        return

    if idx_node.data == "single_index":
        index_val = self.evaluate_expr(idx_node.children[0])
        try:
            # Jika dia adalah array (list), paksa index menjadi angka
            if isinstance(obj, list):
                idx = int(index_val)
                if op_node.type == "EQUAL":
                    obj[idx] = val
                elif op_node.type == "PLUS_EQUAL":
                    obj[idx] += val
                elif op_node.type == "MINUS_EQUAL":
                    obj[idx] -= val
            else:
                # Untuk kamus (dict) nilainya bisa string (huruf)
                if op_node.type == "EQUAL":
                    obj[index_val] = val
                elif op_node.type == "PLUS_EQUAL":
                    obj[index_val] += val
                elif op_node.type == "MINUS_EQUAL":
                    obj[index_val] -= val
        except Exception as e:
            self.error(
                f"Gagal memanipulasi elemen pada [{index_val}] di dalam {var_name}: {e}"
            )
    else:
        self.error(
            "Hanya pengubahan nilai tunggal (single index) yang saat ini didukung pada Assigment!"
        )
