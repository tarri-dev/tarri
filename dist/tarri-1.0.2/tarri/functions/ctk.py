#==============================================================================#
# File    : ctk.py                                                             #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Penulis : Ketut Dana                                                         #
# Kontak  : danayasa2@gmail.com                                                #
# Lisensi : MIT                                                                #
# Situs   : bahasatarri.com                                                    #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Implementasi fungsi bawaan 'ctk' yang tersedia dalam bahasa Tarri.         #
#==============================================================================#

# cetak.py
def ctk(*args, konteks=None):
    if konteks is None:
        konteks = {}

    out = []
    for a in args:
        s = str(a)
        if "{" in s and "}" in s:
            try:
                s = s.format(**konteks)
            except:
                pass
        out.append(s)

    print(" ".join(out))
    return None
