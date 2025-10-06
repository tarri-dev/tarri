# tarri/interpreter/exec_nodes/entry.py
# ==============================================================================#

def exec_entry_point(self, node):
    for stmt in node.children:
        self.exec_node(stmt)