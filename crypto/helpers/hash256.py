import hashlib


def hash256(value):
    return hashlib.sha256(hashlib.sha256(value).digest()).digest()
