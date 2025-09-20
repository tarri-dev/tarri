import time
from datetime import datetime

_trace_stack = []
_db_trace = []

def tipe_data(val):
    if isinstance(val, bool):
        return "logika"
    elif isinstance(val, int) or isinstance(val, float):
        return "angka"
    elif isinstance(val, str):
        return "kata"
    elif val is None:
        return "kosong"
    elif isinstance(val, list):
        return "list"
    else:
        return "tak dikenal"

def trace_step(step_name):
    _trace_stack.append(step_name)

def trace_db(step_info):
    _db_trace.append(step_info)

def print_section(title, content_func, empty_message, bullet="•"):
    """Helper function to print formatted sections"""
    print(f"{title}")
    print("-" * len(title))
    
    content = content_func()
    if not content:
        print(f"  {empty_message}")
    else:
        for item in content:
            print(f"  {bullet} {item}")
    
    print()

def lacak(interpreter, args):
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    raw_val = args[0]

    # cek apakah raw_val adalah nama variable di context
    if isinstance(raw_val, str) and raw_val in interpreter.context:
        val = interpreter.context[raw_val]
        var_name = raw_val
    else:
        val = raw_val
        var_name = "<literal>"

    # Header
    print()
    print(f"LACAK PROSES DATA TARRI")
    print(f"Waktu: {timestamp}")
    print()
    
    # Nilai utama yang sedang dilacak
    print("VARIABLE YANG DILACAK")
    print("---------------------")
    print(f"  Variabel: {var_name}")
    print(f"  Nilai   : {val}")
    print(f"  Tipe    : {tipe_data(val)}")
    print()

    # Semua variable di context
    def get_context_vars():
        return [f"{k} => {v} ({tipe_data(v)})" for k, v in interpreter.context.items()]
    
    print_section(
        "VARIABEL DI SCOPE", 
        get_context_vars, 
        "Tidak ada variable di scope"
    )

    # Call stack
    def get_call_stack():
        return [step for step in _trace_stack]
    
    print_section(
        "CALL STACK", 
        get_call_stack, 
        "Call stack kosong"
    )

    # Database / I/O
    def get_db_trace():
        return [step for step in _db_trace]
    
    print_section(
        "DATABASE / I/O", 
        get_db_trace, 
        "Tidak ada aktivitas DB/I/O"
    )

    # Timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("TIMING")
    print("------")
    print(f"  Eksekusi sampai lacak() = {execution_time:.4f}s")
    print()

    print("Program dihentikan oleh lacak()")
    print()
    
    raise SystemExit("[tarri] Debugging selesai")