import hashlib


def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()
