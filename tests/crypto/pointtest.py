from unittest import TestCase
from crypto.point import Point


class PointTest(TestCase):
    def test_eq(self):
        p1 = Point(18, 77, 5, 7)
        p2 = Point(18, 77, 5, 7)
        p3 = Point(-1, -1, 5, 7)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)

    def test_ne(self):
        p1 = Point(18, 77, 5, 7)
        p2 = Point(18, 77, 5, 7)
        p3 = Point(-1, -1, 5, 7)
        self.assertTrue(p1 != p3)
        self.assertFalse(p1 != p2)

    def test_add(self):
        p1 = Point(18, 77, 5, 7)
        p2 = Point(18, -77, 5, 7)
        inf = Point(None, None, 5, 7)
        self.assertTrue(p1 + inf == p1)
        self.assertTrue(p1 + p2 == inf)
        p1 = Point(2, 5, 5, 7)
        p2 = Point(-1, -1, 5, 7)
        p_result = Point(3, -7, 5, 7)
        self.assertTrue(p1 + p2 == p_result)
        p1 = Point(-1, -1, 5, 7)
        p_result = Point(18, 77, 5, 7)
        self.assertTrue(p1 + p1 == p_result)
        p1 = Point(18, 77, 5, 7)
        p_result = Point('4.248313374936751560', '10.242843069394764453', 5, 7)
        self.assertTrue(p1 + p1 == p_result)
