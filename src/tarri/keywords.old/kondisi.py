# from tarri.keywords import register

# @register("if_stmt")
# def run(interpreter, args):
#     """
#     Keyword 'if_stmt' untuk menangani:'jika', 'ataujika', 'lainnya'
#     """
#     n = len(args)
#     executed = False

#     # kondisi utama "jika"
#     try:
#         condition = interpreter.evaluate_expr(args[0])
#     except Exception:
#         condition = False

#     if condition:
#         interpreter.exec_node(args[1])
#         executed = True
#     else:
#         # cek "ataujika"
#         i = 2
#         while i < n - 1:
#             expr = args[i]
#             block = args[i + 1]
#             try:
#                 cond = interpreter.evaluate_expr(expr)
#             except Exception:
#                 cond = False
#             if cond:
#                 interpreter.exec_node(block)
#                 executed = True
#                 break
#             i += 2

#     # cek "lainnya"
#     if not executed and n % 2 == 1:
#         interpreter.exec_node(args[-1])
