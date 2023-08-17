
def safe_open(f):
    return open(f, "rb") if f is not None else None

def prune_dict(d):
    return {k:v for k, v in d.items() if v is not None}
