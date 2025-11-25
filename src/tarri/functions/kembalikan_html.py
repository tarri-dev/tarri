def kembalikan_html(args, context):
    import re

    if not isinstance(args, (list, tuple)) or len(args) < 2:
        raise Exception("[tarri] kembalikan_html() membutuhkan 2 argumen: (html, penampung)")

    html_template = str(args[0] or "")
    penampung = args[1]

    # Jika penampung kosong, default ke string kosong atau list kosong
    if penampung is None:
        penampung = [] if html_template == "" else ""

    # Ambil variabel dari context aktif interpreter
    env = {}
    env.update(getattr(context, "globals", {}) or {})
    env.update(getattr(context, "context", {}) or {})

    # Regex: tangkap isi di dalam {{ ... }}
    pattern = re.compile(r"\{\{\s*(.*?)\s*\}\}")

    def replace_expr(match):
        expr = match.group(1).strip()
        try:
            # Evaluasi ekspresi di dalam {{ ... }} menggunakan context interpreter
            result = eval(expr, {}, env)
            return str(result) if result is not None else ""
        except Exception as e:
            print(f"[tarri | eval error] {expr} → {e}")
            return "null"

    # Gantikan ekspresi dalam template
    rendered = pattern.sub(replace_expr, html_template)

    # Jika penampung list, tambahkan item baru ke list
    if isinstance(penampung, list):
        if rendered:
            penampung.append(rendered)
        return penampung

    # Jika string, cukup gabungkan
    return str(penampung) + rendered
