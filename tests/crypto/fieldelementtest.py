from unittest import TestCase
from crypto.fieldelement import FieldElement


class FieldElementTest(TestCase):

    def test_eq(self):
        a = FieldElement(11, 71)
        b = FieldElement(11, 71)
        c = FieldElement(7, 71)

        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_ne(self):
        a = FieldElement(11, 71)
        b = FieldElement(11, 71)
        c = FieldElement(7, 71)

        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(14, 17)
        b = FieldElement(7, 17)
        c = FieldElement(4, 17)

        self.assertTrue(a + b == c)

    def test_sub(self):
        a = FieldElement(13, 17)
        b = FieldElement(15, 17)
        c = FieldElement(15, 17)
        self.assertTrue(a - b == c)
        a = FieldElement(13, 17)
        b = FieldElement(1, 17)
        c = FieldElement(12, 17)
        self.assertTrue(a - b == c)

    def test_mul(self):
        a = FieldElement(13, 17)
        b = FieldElement(3, 17)
        c = FieldElement(5, 17)
        self.assertTrue(a * b == c)

    def test_pow(self):
        a = FieldElement(5, 17)
        b = FieldElement(8, 17)
        self.assertTrue(a ** 2 == b)
        a = FieldElement(7, 13)
        b = FieldElement(8, 13)
        self.assertTrue(a ** -3 == b)

    def test_truediv(self):
        a = FieldElement(5, 17)
        b = FieldElement(8, 17)
        c = FieldElement(7, 17)
        self.assertTrue(a / b == c)


