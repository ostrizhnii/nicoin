from crypto.helpers.hash160 import hash160


def op_hash160(stack):
    if len(stack) < 1:
        return False
    stack.append(hash160(stack.pop()))
    return True
