import re

def identify(h):
    length = len(h)
    is_hex = bool(re.match(r'^[a-f0-9]+$', h))

    if h.startswith('$2a$') or h.startswith('$2b$'):
        return 'bcrypt'
    if h.startswith('$1$'):
        return "MD5-crypt"
    if h.startswith('$6$'):
        return "SHA-512-crypt"

    if is_hex:
        if length == 32:
            return 'MD5'
        elif length == 40:
            return 'SHA1'
        elif length == 64:
            return 'SHA256'
        elif length == 128:
            return 'SHA512'
    if h.endswith('='):
        return "Probably Base64 (not a hash!)"

    return "Unknown format"

hash = input("Enter hash: ")
print("Hash: " + identify(hash))
