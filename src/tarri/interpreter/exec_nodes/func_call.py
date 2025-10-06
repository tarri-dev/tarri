from collections import ChainMap

def exec_func_call(self, func_name, args):
    if func_name not in self.functions:
        self.error(f"[tarri | interpreter | func_call] Fungsi '{func_name}' tidak ditemukan")
        return None
    
    params, body = self.functions[func_name]
    local_env = {}
    for i, param in enumerate(params):
        local_env[param] = args[i] if i < len(args) else None

    saved_context = self.context
    saved_return = self._return_flag
    try:
        self.context = ChainMap(local_env, self.globals)
        self._return_flag = None
        result = None
        for stmt in body.children:
            self.exec_node(stmt)
            if self._return_flag is not None:
                result = self._return_flag
                break
        return result
    finally:
        self._return_flag = saved_return
        self.context = saved_context