from lark import Token

def exec_call_expr(self, node):
    func_name_node = node.children[0]
    func_name = func_name_node.value if isinstance(func_name_node, Token) else str(func_name_node)

    args_node = node.children[1] if len(node.children) > 1 else None
    args = []
    if args_node:
        for i, arg in enumerate(args_node.children):
            if func_name == "masukkan" and i == 0:
                args.append(arg)
            else:
                args.append(self.evaluate_expr(arg))

    result = self.exec_func_call(func_name, args)
    # print("[DEBUG CALL EXPR]", func_name, args)
    return result