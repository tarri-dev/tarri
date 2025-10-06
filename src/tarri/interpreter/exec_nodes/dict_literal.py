# tarri/interpreter/exec_nodes/dict_literal.py
# ==============================================================================#

def exec_dict_literal(self, node):
    value = {}
    for pair in node.children:
        key_node = pair.children[0]
        val_node = pair.children[1]

        # ambil key
        if key_node.type == "ESCAPED_STRING":
            key = key_node.value.strip('"')
        else:
            key = key_node.value  # VAR_NAME atau NAME

        # evaluasi value
        val = self.evaluate_expr(val_node)
        value[key] = val

    return value