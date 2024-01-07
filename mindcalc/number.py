from typing import List
from math import isclose


class Number:
    def __repr__(self):
        return f"Number({self.value})"

    def __init__(self, num=None, int_length=None, float_length=None):
        if num is not None:
            self._validate_input(num)
            num = str(num)
            integer_part, float_part = self._split_num(num)
            self._integer_part = self._convert_to_integer_list(integer_part)[::-1]
            self._float_part = self._convert_to_integer_list(float_part)
        elif int_length is not None or float_length is not None:
            self._integer_part = [0] * (int_length if int_length is not None else 0)
            self._float_part = [0] * (float_length if float_length is not None else 0)
        else:
            raise ValueError("Either num or lengths of int and float parts should be provided.")

    @staticmethod
    def _validate_input(num):
        if not isinstance(num, (int, float, str)):
            raise ValueError("Number accepts only numeric types and string type.")

    @staticmethod
    def _split_num(num):
        if '.' in num:
            return num.split('.')
        else:
            return num, '0'

    @staticmethod
    def _convert_to_integer_list(part: str) -> List[int]:
        return [int(digit) for digit in part]

    @property
    def integer_part(self) -> int:
        if len(self._integer_part) > 0:
            return self.get_integer_part()
        else:
            return 0

    @property
    def decimal_part(self) -> int:
        if len(self._float_part) > 0:
            return int("".join(map(str, self._float_part)))
        else:
            return 0

    @property
    def integer_length(self) -> int:
        return len(self._integer_part)

    @property
    def float_length(self) -> int:
        return len(self._float_part)

    def get_integer_part(self):
        return sum(a * 10 ** i for i, a in enumerate(self._integer_part))

    @property
    def value(self) -> float:
        integer_value = self.get_integer_part()
        float_value = sum(a * 10 ** (-i - 1) for i, a in enumerate(self._float_part))
        return float(integer_value + float_value)

    def _number_operation(self, other, operation):
        other = Number(other) if isinstance(other, (int, float, str)) else other
        return Number(operation(self.value, other.value))

    def _integer_operation(self, other, operation):
        other = Number(other) if isinstance(other, (int, float, str)) else other

        if self.decimal_part:
            raise ValueError('Non-integer values cannot be used with this operator.')
        if other.decimal_part:
            raise ValueError('Non-integer values cannot be used with this operator.')

        return Number(operation(self.get_integer_part(), other.get_integer_part()))

    def set_integer_digit(self, digit, index):
        if 0 <= index < len(self._integer_part):
            self._integer_part[index] = digit
        else:
            raise IndexError("Index out of range.")

    def get_integer_digit(self, index):
        if 0 <= index < len(self._integer_part):
            return self._integer_part[index]
        else:
            raise IndexError("Index out of range.")

    def set_float_digit(self, digit, index):
        if 0 <= index < len(self._float_part):
            self._float_part[index] = digit
        else:
            raise IndexError("Index out of range.")

    def get_float_digit(self, index):
        if 0 <= index < len(self._float_part):
            return self._float_part[index]
        else:
            raise IndexError("Index out of range.")

    def __add__(self, other):
        return self._number_operation(other, float.__add__)

    def __sub__(self, other):
        return self._number_operation(other, float.__sub__)

    def __mul__(self, other):
        return self._number_operation(other, float.__mul__)

    def __truediv__(self, other):
        if isinstance(other, (int, float, str)):
            other = Number(other).value
        if other != 0:
            return Number(self.value / other.value)
        else:
            raise ZeroDivisionError("Division by zero is not allowed.")

    def __floordiv__(self, other):
        return self._integer_operation(other, int.__floordiv__)

    def __mod__(self, other):
        return self._integer_operation(other, int.__mod__)

    def __eq__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return isclose(
            self.value, other.value, abs_tol=10 ** -max(self.float_length, other.float_length)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.value > other.value

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.value < other.value

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
