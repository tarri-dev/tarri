def compare(self, op, left, right):
    if op == "==": hasil = left == right
    elif op == "!=": hasil = left != right
    elif op == "<": hasil = left < right
    elif op == ">": hasil = left > right
    elif op == "<=": hasil = left <= right
    elif op == ">=": hasil = left >= right
    else:
        self.error(f"Operator perbandingan tidak dikenal: {op}")
        return "Salah"

    # konversi boolean Python ke Tarri
    if isinstance(hasil, bool):
        return "Benar" if hasil else "Salah"
    return hasil
