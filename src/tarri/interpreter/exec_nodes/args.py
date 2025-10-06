# tarri/interpreter/exec_nodes/args.py
# ==============================================================================#

def exec_args(self, node):
        return [self.exec_node(child) for child in node.children]


