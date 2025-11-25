from lark import Tree, Token

# def exec_func_decl(self, node):
#     func_name = node.children[0].value
#     params_node = node.children[1] if len(node.children) > 1 else None
#     params = []
#     if isinstance(params_node, Tree) and params_node.data == "params":
#         for p in params_node.children:
#             if isinstance(p, Tree) and p.data == "param" and p.children:
#                 child = p.children[0]
#                 params.append(child.value if isinstance(child, Token) else str(child))
#             elif isinstance(p, Token):
#                 params.append(p.value)
#     body = node.children[-1]
#     self.functions[func_name] = (params, body)
#     if self.status:
#         return None


def exec_func_decl(self, node):
    func_name = node.children[0].value
    params_node = node.children[1] if len(node.children) > 1 else None
    params = []
    if isinstance(params_node, Tree) and params_node.data == "params":
        for p in params_node.children:
            if isinstance(p, Tree) and p.data == "param" and p.children:
                child = p.children[0]
                params.append(child.value if isinstance(child, Token) else str(child))
            elif isinstance(p, Token):
                params.append(p.value)
    body = node.children[-1]
    
    # Simpan ke functions
    self.functions[func_name] = (params, body)

    # ⚡ Tambahkan ke context supaya bisa dipanggil dari rute
    def func(*args):
        # Bisa pakai argumen nanti kalau diperlukan
        old_return_flag = getattr(self, "_return_flag", None)
        self._return_flag = None
        try:
            self.exec_node(body)
        finally:
            result = self._return_flag
            self._return_flag = old_return_flag
        return result
    
    self.context[func_name] = func

    if getattr(self, "status", None):
        return None
