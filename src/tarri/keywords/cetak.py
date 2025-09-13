from tarri.keywords import register

@register("print_stmt")  # pakai nama rule grammar
def run(interpreter, args):
    """Keyword cetak untuk menampilkan output ke layar"""

    outputs = []
    for value_node in args:
        # Evaluasi node ke nilai asli (bukan token mentah)
        val = interpreter.evaluate_expr(value_node)
        outputs.append(str(val) if val is not None else "")

    # pakai flush=True biar tidak ketahan buffer saat ada input()
    print(" ".join(outputs), flush=True)
