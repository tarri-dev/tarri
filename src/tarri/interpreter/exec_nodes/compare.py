def compare(self, op, left, right):
    if op == "==": return left == right
    if op == "!=": return left != right
    if op == "<": return left < right
    if op == ">": return left > right
    if op == "<=": return left <= right
    if op == ">=": return left >= right
    self.error(f"Operator perbandingan tidak dikenal: {op}")
    return False