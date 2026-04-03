#==============================================================================#
# File    : compare.py                                                         #
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
#   'compare' dalam penerjemah Tarri.                                          #
#==============================================================================#

# def compare(self, op, left, right):
#     if op == "==": hasil = left == right
#     elif op == "!=": hasil = left != right
#     elif op == "<": hasil = left < right
#     elif op == ">": hasil = left > right
#     elif op == "<=": hasil = left <= right
#     elif op == ">=": hasil = left >= right
#     else:
#         self.error(f"Operator perbandingan tidak dikenali: {op}")
#         return "Salah"

#     # konversi boolean Python ke Tarri
#     if isinstance(hasil, bool):
#         return "Benar" if hasil else "Salah"
#     return hasil


def compare(self, op, left, right):
    # Pastikan operand diubah menjadi nilai dasarnya (misalnya, string)
    if hasattr(left, "kata"):
        left = left.kata()
    if hasattr(right, "kata"):
        right = right.kata()

    # Lakukan perbandingan, hasilnya adalah nilai Boolean (True atau False)
    if op == "==":
        hasil = left == right
    elif op == "!=":
        hasil = left != right
    elif op == "<":
        hasil = left < right
    elif op == ">":
        hasil = left > right
    elif op == "<=":
        hasil = left <= right
    elif op == ">=":
        hasil = left >= right
    else:
        # Menangani operator yang tidak dikenal
        self.error(f"Operator perbandingan tidak dikenal: {op}")
        # Mengembalikan nilai yang pasti False dalam konteks Boolean untuk mencegah eksekusi if
        return False

    # --- BARIS KRITIS YANG DIPERBAIKI ---
    # Mengembalikan nilai Boolean 'hasil' (True atau False)
    # Ini memastikan bahwa 'jika' (if) Tarri mengevaluasi kondisi dengan benar.
    return hasil
