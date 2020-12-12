from crypto.point import Point
from crypto.s256fieldelement import S256FieldElement, P

N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
A = 0
B = 7


class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a = S256FieldElement(A)
        b = S256FieldElement(B)
        if type(x) == int:
            super().__init__(S256FieldElement(x), S256FieldElement(y), a, b)
        else:
            super().__init__(x, y, a, b)

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        return 'S256Point({}, {})'.format(self.x, self.y)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        target = u * G + v * self
        return target.x.num == sig.r

    def sec(self, compressed=True):
        if compressed:
            marker = b'\x02' if self.y.num % 2 == 0 else b'\x03'
            return marker + self.x.num.to_bytes(32, 'big')

        return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    @classmethod
    def parse(cls, sec_bin):
        marker = sec_bin[0]
        if marker == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return cls(x, y)
        x = S256FieldElement(int.from_bytes(sec_bin[1:], 'big'))
        # right side of the equation y^2 = x^3 + 7
        alpha = x ** 3 + S256FieldElement(B)
        # solving left side of the equation y^2 = x^3 + 7
        beta = alpha.sqrt()
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256FieldElement(P - beta.num)
        else:
            even_beta = S256FieldElement(P - beta.num)
            odd_beta = beta
        if marker == 2:
            return cls(x, even_beta)
        else:
            return cls(x, odd_beta)


G = S256Point(GX, GY)
