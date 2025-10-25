
# tarri/interpreter/exec_nodes/auto_var_decl.py
# ==============================================================================#

def exec_auto_var_decl(self, node):
    var_name = node.children[0].value
    op_node = node.children[1] if len(node.children) > 1 else None
    value_node = node.children[2] if len(node.children) > 2 else None
    value = self.evaluate_expr(value_node) if value_node is not None else None

    if op_node.type == "EQUAL":
        self.context[var_name] = value
    elif op_node.type == "PLUS_EQUAL":
        if isinstance(value, list):
            self.context[var_name] = self.context.get(var_name, []) + value
        else:
            self.context[var_name] = self.context.get(var_name, 0) + value
    elif op_node.type == "MINUS_EQUAL":
        self.context[var_name] = self.context.get(var_name, 0) - value
    else:
        self.error(f"[tarri | interpreter | auto_var_decl] Operator assignment tidak dikenal: {op_node.value}")

    # print("[DEBUG VAR DECL]", var_name, "=", value)
    # print("[DEBUG EVAL VALUE]", value, type(value))
    return self.context[var_name]