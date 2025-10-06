# exec_nodes/loop_stmt.py
"""
Loop execution helpers for Tarri.
Contains:
 - BreakSignal / ContinueSignal
 - exec_break_stmt, exec_continue_stmt
 - exec_loop_stmt (robust handling for many loop AST shapes)
"""

# Exceptions used for control flow inside loops
class BreakSignal(Exception):
    """Sinyal untuk keluar dari loop (break)."""
    pass

class ContinueSignal(Exception):
    """Sinyal untuk lanjut ke iterasi berikutnya (continue)."""
    pass


def exec_break_stmt(self, node):
    """Handler untuk break_stmt -> lemparkan BreakSignal"""
    raise BreakSignal()


def exec_continue_stmt(self, node):
    """Handler untuk continue_stmt -> lemparkan ContinueSignal"""
    raise ContinueSignal()


def exec_loop_stmt(self, node):
    """Eksekusi semua jenis loop di Tarri.

    Modul ini mencoba mengenali beberapa pola AST yang umum:
    - ulangi { block }                (unconditional infinite loop)
    - VAR = start end block           (numeric range loop)
    - VAR list_literal block          (iterate list literal)
    - selama expr block               (while loop)
    - setiap VAR dari expr block      (for-each)
    - setiapdari VAR = start hingga end dari step block  (range with step)
    - untuk VAR dalam expr block      (for ... in)
    - shorthand foreach: VAR VAR block  (ambil iterable dari context)
    """
    children = node.children

    def get_var_name(token_or_node):
        # Ambil nama variabel dari Token atau Tree
        if hasattr(token_or_node, "value"):  # Token
            return token_or_node.value
        if hasattr(token_or_node, "children") and token_or_node.children:
            return get_var_name(token_or_node.children[0])
        return str(token_or_node)

    # ---------- CASE A: "ulangi { ... }" (single block) ----------
    if len(children) == 1 and hasattr(children[0], "data") and children[0].data == "block":
        block = children[0]
        while True:
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # ---------- CASE B: Numeric range -> VAR_NAME '=' start end block ----------
    if (
        len(children) >= 5
        and getattr(children[0], "type", None) == "VAR_NAME"
        and getattr(children[1], "type", None) == "EQUAL"
        and hasattr(children[-1], "data") and children[-1].data == "block"
    ):
        var_name = get_var_name(children[0])
        start_val = self.evaluate_expr(children[2])
        end_val = self.evaluate_expr(children[3])
        block = children[-1]

        # support integer-like iteration
        i = start_val
        while i <= end_val:
            self.context[var_name] = i
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                i += 1
                continue
            i += 1
        return

    # ---------- CASE C: "VAR list_literal block" ----------
    if (
        len(children) == 3
        and getattr(children[0], "type", None) == "VAR_NAME"
        and hasattr(children[1], "data") and children[1].data == "list_literal"
        and hasattr(children[2], "data") and children[2].data == "block"
    ):
        var_name = get_var_name(children[0])
        iterable = self.evaluate_expr(children[1])
        block = children[2]

        if iterable is None or not hasattr(iterable, "__iter__"):
            self.error("Target loop bukan iterable")
            return

        for item in iterable:
            self.context[var_name] = item
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # ---------- CASE D: "selama expr block"  (while) ----------
    # Two common shapes:
    #  1) [Token('SELAMA','selama'), expr, block]
    #  2) [expr, block]
    if getattr(children[0], "type", None) == "SELAMA" and len(children) >= 3 and hasattr(children[2], "data") and children[2].data == "block":
        condition = children[1]
        block = children[2]
        while self.evaluate_expr(condition):
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    if len(children) == 2 and hasattr(children[1], "data") and children[1].data == "block":
        # fallback: bentuk [expr, block]
        condition = children[0]
        block = children[1]
        while self.evaluate_expr(condition):
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # ---------- CASE E: "setiap VAR dari expr block" ----------
    if (
        len(children) >= 5
        and getattr(children[0], "type", None) == "SETIAP"
        and getattr(children[1], "type", None) == "VAR_NAME"
        and hasattr(children[4], "data") and children[4].data == "block"
    ):
        var_name = get_var_name(children[1])
        iterable = self.evaluate_expr(children[3])
        block = children[4]

        if iterable is None or not hasattr(iterable, "__iter__"):
            self.error("Target 'setiap' bukan iterable")
            return

        for item in iterable:
            self.context[var_name] = item
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # ---------- CASE F: "setiapdari VAR = start hingga end dari step block" ----------
    if (
        len(children) == 6
        and getattr(children[0], "type", None) == "VAR_NAME"
        and getattr(children[1], "type", None) == "EQUAL"
        and hasattr(children[5], "data") and children[5].data == "block"
    ):
        var_name = get_var_name(children[0])
        start_val = self.evaluate_expr(children[2])
        end_val = self.evaluate_expr(children[3])
        step_val = self.evaluate_expr(children[4])
        block = children[5]

        if step_val == 0:
            self.error("Step pada 'setiapdari' tidak boleh nol")
            return

        i = start_val
        if step_val > 0:
            while i <= end_val:
                self.context[var_name] = i
                try:
                    self.exec_node(block)
                except BreakSignal:
                    break
                except ContinueSignal:
                    i += step_val
                    continue
                i += step_val
        else:
            while i >= end_val:
                self.context[var_name] = i
                try:
                    self.exec_node(block)
                except BreakSignal:
                    break
                except ContinueSignal:
                    i += step_val
                    continue
                i += step_val
        return

    # ---------- CASE G: "untuk VAR dalam expr block" ----------
    if (
        len(children) >= 5
        and getattr(children[0], "type", None) == "UNTUK"
        and getattr(children[1], "type", None) == "VAR_NAME"
        and hasattr(children[4], "data") and children[4].data == "block"
    ):
        var_name = get_var_name(children[1])
        iterable = self.evaluate_expr(children[3])
        block = children[4]

        if iterable is None or not hasattr(iterable, "__iter__"):
            self.error("Target 'untuk' bukan iterable")
            return

        for item in iterable:
            self.context[var_name] = item
            try:
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # ---------- CASE H: shorthand "VAR VAR block" -> ambil iterable dari context ----------
    if (
        len(children) == 3
        and getattr(children[0], "type", None) == "VAR_NAME"
        and getattr(children[1], "type", None) == "VAR_NAME"
        and hasattr(children[2], "data") and children[2].data == "block"
    ):
        var_name = children[0].value
        iterable_name = children[1].value

        # prioritas: ambil dari context jika ada, kalau tidak evaluate ekspresi
        iterable = self.context.get(iterable_name, None)
        if iterable is None:
            iterable = self.evaluate_expr(children[1])

        block = children[2]

        if not hasattr(iterable, "__iter__"):
            raise Exception(f"[tarri | interpreter | loop_stmt] {iterable_name} bukan iterable")

        for item in iterable:
            try:
                self.context[var_name] = item
                # gunakan exec_node agar dispatch consistent
                self.exec_node(block)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return

    # -------------------------
    # Fallback: unknown loop shape
    # -------------------------
    self.error(f"[tarri | interpreter | loop_stmt] Tidak tahu cara eksekusi loop_stmt: {children}")
