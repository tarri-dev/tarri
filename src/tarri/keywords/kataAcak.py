import random
import string
from . import register

@register("kataAcak")  # HARUS sama dengan identifier di AST
def run(interpreter, args):
    panjang = interpreter.evaluate_expr(args[0])
    if not isinstance(panjang, int) or panjang <= 0:
        interpreter.error(f"Argumen kataAcak harus angka positif, bukan {panjang}")
        return ""

    return "".join(random.choices(string.ascii_lowercase, k=panjang))
