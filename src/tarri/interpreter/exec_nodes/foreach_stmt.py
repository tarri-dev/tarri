

def exec_foreach_stmt(self, node):
    var_name = node.children[0].value
    iterable = self.evaluate_expr(node.children[1])
    for item in iterable:
        self._ctx[var_name] = item
        self.exec_block(node.children[2])