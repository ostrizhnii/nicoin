from crypto.helpers.numendian import int_to_bit_endian


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

    def der(self):
        rbin = int_to_bit_endian(self.r)
        rbin = rbin.lstrip(b'\x00')
        if rbin[0] & 0x80:
            rbin = '\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = int_to_bit_endian(self.r)
        sbin = sbin.lstrip(b'\x00')
        if sbin[0] & 0x80:
            sbin = '\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result
