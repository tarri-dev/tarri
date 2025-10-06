import time

_trace_stack = []
_db_trace = []


def tipe_data(val):
    """Deteksi tipe data khas TARRI."""
    try:
        from tarri.session.sesi import SesiObj
        if isinstance(val, SesiObj):
            return "sesi"
    except Exception:
        pass

    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, (int, float)):
        return "angka"
    elif isinstance(val, str):
        return "kata"
    elif val is None:
        return "kosong"
    elif isinstance(val, list):
        return "list"
    elif isinstance(val, dict):
        return "kamus"
    else:
        return "tak dikenal"


def garis():
    """Bikin garis pembatas horizontal."""
    return "─" * 60


def print_box(title, lines):
    """Tampilkan section dengan gaya kotak minimalis di terminal."""
    print(f"┌─ {title}")
    for line in lines:
        print(f"│ {line}")
    print("└" + garis())


def format_value(v):
    """Format nilai supaya tampil bagus di terminal."""
    try:
        from tarri.session.sesi import SesiObj
        if isinstance(v, SesiObj):
            # kalau sesi bisa dikonversi ke dict
            if hasattr(v, "to_dict"):
                data = v.to_dict()
                info = [f"{k} : {val}" for k, val in data.items()]
                formatted = "[Sesi aktif]\n" + "\n".join([" " * 14 + line for line in info])
                return formatted
            return "[Sesi aktif]"
    except Exception:
        pass

    if isinstance(v, dict):
        items = [f"{k} => {val}" for k, val in v.items()]
        return "{ " + ", ".join(items) + " }"
    elif isinstance(v, list):
        return "[" + ", ".join(map(str, v)) + "]"
    else:
        return str(v)


def lacak(interpreter, args):
    """Menampilkan data yang sedang dilacak secara terstruktur."""
    start_time = time.time()

    raw_val = args[0]
    if isinstance(raw_val, str) and raw_val in interpreter.context:
        val = interpreter.context[raw_val]
        var_name = raw_val
    else:
        val = raw_val
        var_name = "<literal>"

    print()
    print("╭────────────────────────────────────────────────────────────╮")
    print("│                LACAK PROSES DATA TARRI                     │")
    print("│                ======================                      │")
    print("╰────────────────────────────────────────────────────────────╯")
    print()

    # Nilai utama yang sedang dilacak
    lines = [
        f"Variabel : {var_name}",
        f"Nilai    : {val}",
        f"Tipe     : {tipe_data(val)}"
    ]
    print_box("VARIABLE YANG DILACAK", lines)

    # Semua variable di context
    context_items = interpreter.context.items()
    if context_items:
        context_lines = [
            f"{k:<12} => {format_value(v)} ({tipe_data(v)})"
            for k, v in context_items
        ]
    else:
        context_lines = ["Tidak ada variabel di scope."]
    print_box("VARIABEL DI SCOPE", context_lines)

    # Call stack
    stack_lines = _trace_stack or ["(kosong)"]
    print_box("CALL STACK", stack_lines)

    # Database / I/O
    db_lines = _db_trace or ["Tidak ada aktivitas DB/I/O."]
    print_box("DATABASE / I/O", db_lines)

    # Timing
    execution_time = time.time() - start_time
    timing_lines = [f"Eksekusi sampai lacak() : {execution_time:.4f} detik"]
    print_box("TIMING", timing_lines)

    print("Program dihentikan oleh lacak()")
    print()
    raise SystemExit("[tarri | lacak] Lacak data selesai")
