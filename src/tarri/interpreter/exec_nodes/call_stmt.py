from lark import Tree, Token

def exec_call_stmt(self, node):
    func_node = node.children[0]
    func_name = None
    if isinstance(func_node, Token):
        func_name = func_node.value
    elif isinstance(func_node, Tree) and func_node.data == "identifier" and func_node.children:
        first = func_node.children[0]
        func_name = first.value if isinstance(first, Token) else str(first)
    else:
        func_name = str(func_node)
    args = []
    if len(node.children) > 1:
        maybe_args = node.children[1]
        if isinstance(maybe_args, Tree) and maybe_args.data == "args":
            for a in maybe_args.children:
                args.append(self.evaluate_expr(a))
        else:
            for a in node.children[1:]:
                args.append(self.evaluate_expr(a))
    return self.call_function(func_name, args)