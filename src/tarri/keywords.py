KEYWORDS = {}

def register(name):
    def decorator(func):
        KEYWORDS[name] = func
        return func
    return decorator
