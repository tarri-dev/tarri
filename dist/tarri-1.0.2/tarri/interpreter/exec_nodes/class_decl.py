#==============================================================================#
# File    : class_decl.py                                                      #
# Proyek  : Bahasa TARRI versi 0.8.x                                           #
#           Teknologi Algoritmik Representasi Rekayasa Indonesia               #
#------------------------------------------------------------------------------#
# Deskripsi :                                                                  #
#   Executor untuk deklarasi kelas 'kelas ... [perluas ...] { ... }'           #
#==============================================================================#

from lark import Tree, Token


class TarriInstance:
    def __init__(self, cls):
        self.__class_obj__ = cls
        self.__dict__["_kelas"] = cls.name
        # salin atribut default
        for k, v in getattr(cls, "attrs", {}).items():
            self.__dict__[k] = v

    def __getattr__(self, name):
        cls = getattr(self, "__class_obj__", None)
        if cls is None:
            raise AttributeError(name)
        # cari metode di class + parent
        method = cls.get_method(name)
        if method is not None:
            # bind method
            def bound(*args, **kwargs):
                return method(self, *args, **kwargs)
            return bound
        raise AttributeError(f"Objek tidak memiliki atribut/metode '{name}'")

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __str__(self):
        return f"<objek {getattr(self.__class_obj__, 'name', 'Kelas')}>"


class TarriClass:
    def __init__(self, name, parent=None, methods=None, attrs=None, body=None):
        self.name = name
        self.parent = parent
        self.methods = methods or {}
        self.attrs = attrs or {}
        self.body = body

    def get_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.parent is not None:
            return self.parent.get_method(name)
        return None

    def get_attr(self, name):
        if name in self.attrs:
            return self.attrs[name]
        if self.parent is not None:
            return self.parent.get_attr(name)
        return None


def exec_class_decl(self, node):
    # class_decl: "kelas" NAME ["perluas" NAME] block
    children = node.children
    class_name = None
    parent_name = None
    body = None

    for c in children:
        if isinstance(c, Token):
            if c.type == "NAME" and class_name is None:
                class_name = c.value
            elif c.type == "NAME" and class_name is not None and parent_name is None:
                parent_name = c.value
        elif isinstance(c, Tree):
            if c.data in ("block", "class_block"):
                body = c
            elif c.data == "NAME" and hasattr(c, "value"):
                pass

    if class_name is None and children:
        # coba ambil dari token pertama
        for c in children:
            if isinstance(c, Token) and getattr(c, 'value') and c.value not in ['perluas']:
                class_name = c.value
                break

    parent_cls = None
    if parent_name:
        parent_cls = self.classes.get(parent_name) or self.functions.get(parent_name)
        # juga bisa disimpan di context
        if parent_cls is None and hasattr(self, 'context'):
            pcand = self.context.get(parent_name)
            if isinstance(pcand, TarriClass):
                parent_cls = pcand

    methods = {}
    attrs = {}

    if body is not None:
        for stmt in body.children:
            if not isinstance(stmt, Tree):
                continue
            if stmt.data == "func_decl":
                # ekstrak nama fungsi & params & body
                schildren = stmt.children
                fname = None
                params_node = None
                fbody = None
                for sc in schildren:
                    if isinstance(sc, Token) and sc.type in ("NAME",):
                        if fname is None:
                            fname = sc.value
                    elif isinstance(sc, Tree):
                        if sc.data == "params":
                            params_node = sc
                        elif sc.data == "block":
                            fbody = sc
                if fname is None and schildren:
                    # fallback
                    for sc in schildren:
                        if isinstance(sc, Token):
                            fname = sc.value
                            break
                params = []
                if isinstance(params_node, Tree):
                    for p in params_node.children:
                        if isinstance(p, Tree) and p.data == "param" and p.children:
                            ch = p.children[0]
                            if isinstance(ch, Token):
                                params.append(ch.value)
                        elif isinstance(p, Token):
                            params.append(p.value)
                if fbody is not None and fname is not None:
                    # buat fungsi terikat
                    def make_method(method_name, method_params, method_body):
                        def method(self_obj, *args):
                            # buat scope baru
                            old_return = getattr(self, "_return_flag", None)
                            self._return_flag = None
                            # push scope
                            if hasattr(self, "env_stack"):
                                self.env_stack.append({})
                            else:
                                self.env_stack = [{}]
                            # set diri/ini
                            try:
                                self.set_var("diri", self_obj)
                                self.set_var("ini", self_obj)
                                # bind params (skip self)
                                call_args = list(args)
                                for i, pname in enumerate(method_params):
                                    if i == 0 and pname in ("diri", "ini", "self"):
                                        # sudah diset
                                        continue
                                    if i < len(call_args):
                                        self.set_var(pname, call_args[i])
                                    else:
                                        self.set_var(pname, None)
                                self.exec_node(method_body)
                            finally:
                                result = getattr(self, "_return_flag", None)
                                self._return_flag = old_return
                                if hasattr(self, "env_stack") and self.env_stack:
                                    self.env_stack.pop()
                            return result
                        return method
                    methods[fname] = make_method(fname, params, fbody)
            elif stmt.data == "auto_var_decl":
                # atribut default
                try:
                    # evaluasi nilai default
                    schildren = stmt.children
                    if len(schildren) >= 3:
                        vname = schildren[0].value if isinstance(schildren[0], Token) else str(schildren[0])
                        valnode = schildren[2]
                        val = self.evaluate_expr(valnode)
                        attrs[vname] = val
                except Exception:
                    pass

    cls = TarriClass(class_name, parent=parent_cls, methods=methods, attrs=attrs, body=body)
    if not hasattr(self, "classes"):
        self.classes = {}
    self.classes[class_name] = cls
    if hasattr(self, "context"):
        self.context[class_name] = cls
    # juga daftarkan bisa dipanggil sebagai konstruktor
    self.functions[class_name] = cls
    return cls
