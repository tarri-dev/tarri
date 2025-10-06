# tarri/interpreter/exec_nodes/exec_list_literal.py
# ==============================================================================#

def exec_list_literal(self, node):
    hasil = []
    for child in node.children:
        nilai = self.exec_node(child)
        hasil.append(nilai)
    return hasil