import string
import secrets


def huruf_acak(length):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    try:
        length = int(length)
    except ValueError:
        length = 5
    return ''.join(secrets.choice(chars) for _ in range(length))
