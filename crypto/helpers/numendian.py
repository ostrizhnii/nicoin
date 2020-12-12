def big_endian_to_int(b):
    return int.from_bytes(b, 'big')


def int_to_bit_endian(num, length=32):
    return num.to_bytes(length, 'big')


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(num, length=32):
    return num.to_bytes(length, 'little')
