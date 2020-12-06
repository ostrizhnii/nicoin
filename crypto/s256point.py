from crypto.point import Point
from crypto.s256fieldelement import S256FieldElement
from crypto.secp256k1 import A, B, N, GX, GY


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


G = S256Point(GX, GY)
