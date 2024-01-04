import unittest

from .leapyear import is_leapyear


class LeapyearShould(unittest.TestCase):

    def test_return_false_for_numbers_not_divisible_by_4(self):
        numbers = [3, 1997]

        def test(year):
            self.assertFalse(is_leapyear(year))

        for n in numbers:
            with self.subTest(n=n):
                test(n)

    def test_return_true_for_numbers_divisible_by_4_but_not_100(self):
        numbers = [4, 1996]

        def test(year):
            self.assertTrue(is_leapyear(year))

        for n in numbers:
            with self.subTest(n=n):
                test(n)

    def test_return_false_for_numbers_divisible_by_100(self):
        numbers = [100, 1800]

        def test(year):
            self.assertFalse(is_leapyear(year))

        for n in numbers:
            with self.subTest(n=n):
                test(n)

    def test_return_true_for_numbers_divisible_by_400(self):
        numbers = [400, 2000]

        def test(year):
            self.assertTrue(is_leapyear(year))

        for n in numbers:
            with self.subTest(n=n):
                test(n)

    def test_return_true_for_0(self):
        self.assertTrue(is_leapyear(0))

    def test_raise_type_error_on_string(self):
        self.assertRaises(TypeError, lambda: is_leapyear("1996"))

    def test_raise_value_error_on_non_integer_number(self):
        self.assertRaises(ValueError, lambda: is_leapyear(1996.2))
