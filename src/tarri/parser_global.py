import os
from lark import Lark

_GLOBAL_ENV = {}

# tarri/src/tarri/parser_global.py
from tarri.session.sesi import sesi as sesi_py


def set_env(key, value):
    _GLOBAL_ENV[key] = value

def get_env(key):
    return _GLOBAL_ENV.get(key)


# Path grammar
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
    tarri_grammar = f.read()

# Parser global
parser = Lark(tarri_grammar, start="start", parser="lalr")
