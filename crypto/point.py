from decimal import *


class Point:
    def __init__(self, x, y, a, b):
        getcontext().prec = 20
        self.x = Decimal(x) if x is not None else x
        self.y = Decimal(y) if y is not None else y
        self.a = Decimal(a) if a is not None else a
        self.b = Decimal(b) if b is not None else b
        if self.x is None and self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        return 'Point({}, {})_{}_{}'.format(self.x, self.y, self.a, self.b)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != self.b:
            raise ValueError('Points {} and {} are not on the same curve'.format(self, other))
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x = (slope ** 2) - self.x - other.x
            y = slope * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        if self == other:
            slope = (3 * (self.x ** 2) + self.a) / (2 * self.y)
            x = (slope ** 2) - 2 * self.x
            y = slope * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        return self.__class__(self.x + other.x, self.y + other.y, self.a, self.b)

