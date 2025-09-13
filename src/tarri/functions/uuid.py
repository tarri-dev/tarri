import uuid

def UUID():
    """
    Menghasilkan UUID versi 4 (acak)
    """
    return str(uuid.uuid4())

# cara menggunakan UUID()
# titikawal{
#     _id = UUID()
#     cetak _id
# }
