from unittest import TestCase
from crypto.fieldelement import FieldElement
from crypto.point import Point


class EecTest(TestCase):
    def test_field_elements_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192, 105), (17, 56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add_for_field_points(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        p1 = Point(FieldElement(170, prime), FieldElement(142, prime), a, b)
        p2 = Point(FieldElement(60, prime), FieldElement(139, prime), a, b)
        p_result = Point(FieldElement(220, prime), FieldElement(181, prime), a, b)
        self.assertTrue(p1 + p2 == p_result)
        p1 = Point(FieldElement(47, prime), FieldElement(71, prime), a, b)
        p2 = Point(FieldElement(17, prime), FieldElement(56, prime), a, b)
        p_result = Point(FieldElement(215, prime), FieldElement(68, prime), a, b)
        self.assertTrue(p1 + p2 == p_result)
        p1 = Point(FieldElement(143, prime), FieldElement(98, prime), a, b)
        p2 = Point(FieldElement(76, prime), FieldElement(66, prime), a, b)
        p_result = Point(FieldElement(47, prime), FieldElement(71, prime), a, b)
        self.assertTrue(p1 + p2 == p_result)

