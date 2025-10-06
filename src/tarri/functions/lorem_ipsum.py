import random

_LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut "
    "labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris "
    "nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit "
    "esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in "
    "culpa qui officia deserunt mollit anim id est laborum"
).split()

def lorem_ipsum(jumlah=20):
    """Menghasilkan string Lorem Ipsum acak sepanjang jumlah kata."""
    try:
        jumlah = int(jumlah)
    except ValueError:
        jumlah = 20
    return ' '.join(random.choices(_LOREM_WORDS, k=jumlah))
