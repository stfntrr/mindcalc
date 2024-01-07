import unittest
from mindcalc.number import Number

class TestNumber(unittest.TestCase):
    def setUp(self):
        self.num = Number(3.14)

    def test_repr(self):
        self.assertEqual(repr(self.num), "Number(3.14)")

    def test_init(self):
        self.assertIsInstance(self.num, Number)

    def test_get_integer_part(self):
        self.assertEqual(self.num.get_integer_part(), 3)

    def test_get_value(self):
        self.assertEqual(self.num.value, 3.14)

    def test_add(self):
        self.assertEqual((self.num + Number(1.86)).value, 5.0)

    def test_sub(self):
        self.assertEqual((self.num - Number(1)).value, 2.14)

    def test_mul(self):
        self.assertEqual((self.num * Number(2)).value, 6.28)

    def test_truediv(self):
        with self.assertRaises(ZeroDivisionError):
            self.num / Number(0)
        self.assertEqual((self.num / Number(2)).value, 1.57)

    def test_floordiv(self):
        self.assertEqual((Number(10) // Number(3)).value, 3.0)

    def test_mod(self):
        self.assertEqual((Number(10) % Number(3)).value, 1.0)

    def test_initialize_by_digit_length(self):
        num = Number(int_length=4, float_length=2)
        self.assertEqual(repr(num), "Number(0.0)")

    def test_set_get_integer_digit(self):
        num = Number(int_length=4)
        num.set_integer_digit(5, 1)
        self.assertEqual(num.get_integer_digit(1), 5)

    def test_set_get_float_digit(self):
        num = Number(float_length=2)
        num.set_float_digit(4, 0)
        self.assertEqual(num.get_float_digit(0), 4)


if __name__ == '__main__':
    unittest.main()