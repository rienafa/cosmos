import hashlib

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def ibc_denom(path):
    to_hash = f"{path['path']}/{path['base_denom']}"
    return f"ibc/{sha256(to_hash).swapcase()}"

def prety_print(d):
    print(json.dumps(d, indent=4))