from crypto.point import Point
from crypto.s256fieldelement import S256FieldElement


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


G = S256Point(GX, GY)
