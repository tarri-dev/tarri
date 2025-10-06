# tarri/interpreter/exec_nodes/block.py
# ==============================================================================#
# block.py - menangani blok kode (block) → biasanya { ... } 
# atau satu grup statement dalam fungsi, loop, atau conditional.
# ==============================================================================#

# from tarri.interpreter.core import Context  # Optional, kalau perlu akses Context

def exec_block(self, node):
    result = None
    for stmt in node.children:
        if self._return_flag is not None:
            break
        val = self.exec_node(stmt)
        if self._return_flag is not None:
            result = val
            break
    return result