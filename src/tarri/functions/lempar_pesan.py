#==============================================================================#
# File    : lempar_pesan.py                                                    #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'lempar_pesan' yang tersedia dalam bahasa       #
#   Tarri.                                                                     #
#==============================================================================#

def lempar_pesan(pesan):
    """Lempar kesalahan ke sistem coba/tangkap."""
    raise Exception(str(pesan))
