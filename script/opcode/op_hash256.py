from crypto.helpers.hash256 import hash256


def op_hash256(stack):
    if len(stack) < 1:
        return False
    stack.append(hash256(stack.pop()))
    return True
