from lark import Tree
from tarri.keywords import KEYWORDS

def exec_node(self, node):
    if not isinstance(node, Tree):
        return None

    # Container node → eksekusi anak-anak
    if node.data in ("start", "entry_point", "block"):
        for child in node.children:
            self.exec_node(child)
        return None

    # Keyword chaining grammar → handler dari KEYWORDS
    if node.data in KEYWORDS:
        handler = KEYWORDS[node.data]
        return handler(self, node.children)

    # Fallback ke method exec_{tipe}
    handler_name = f"exec_{node.data}"
    if hasattr(self, handler_name):
        return getattr(self, handler_name)(node)

    # Ekspresi literal umum
    if node.data == "expr_stmt":
        return self.evaluate_expr(node.children[0]) if node.children else None
    if node.data == "method_call_expr":
        return self.evaluate_expr(node)

    self.error(f"[tarri | exec_node]Tidak tahu cara eksekusi {node.data}")
    return None
