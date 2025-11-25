# cetak.py
def cetak(*args, konteks=None):
    if konteks is None:
        konteks = {}

    out = []
    for a in args:
        s = str(a)
        if "{" in s and "}" in s:
            try:
                s = s.format(**konteks)
            except:
                pass
        out.append(s)

    print(" ".join(out))
    return None
