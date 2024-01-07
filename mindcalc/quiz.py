from enum import Enum
from math import isclose

from .number import Number
from random import randint


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Quiz:
    operations = {'+': '__add__', '-': '__sub__', '*': '__mul__', '/': '__truediv__'}

    def __init__(self, int_length: int, float_length: int, difficulty: Difficulty):
        self.int_length = int_length
        self.float_length = float_length
        self.difficulty = difficulty
        self.history = []

        self._num1 = Number(0)
        self._num2 = Number(0)

    def get_numbers(self) -> tuple[float, float]:
        self._num1 = self._generate_number()
        self._num2 = self._generate_related_number()
        return self._num1.value, self._num2.value

    def _generate_number(self) -> Number:
        int_part = randint(10 ** (self.int_length - 1), 10 ** self.int_length - 1)
        float_part = randint(10 ** (self.float_length - 1), 10 ** self.float_length - 1) / 10 ** self.float_length
        return Number(int_part + float_part)
    def _generate_related_number(self) -> Number:
        pass  # Placeholder, you should implement this

    @property
    def correct_answer(self):
        return getattr(self._num1, self.operations[self.operation])(self._num2).value

    def check_answer(self, user_answer, start_time, end_time):
        correct = round(user_answer, 6) == round(self.correct_answer, 6)
        self.history.append({
            'num1': self._num1,
            'operation': self.operation,
            'num2': self._num2,
            'user_answer': user_answer,
            'correct_answer': self.correct_answer,
            'correct': correct,
            'time': end_time - start_time
        })
        return correct


class AdditionQuiz(Quiz):
    def __init__(self, int_length: int, float_length: int, difficulty: Difficulty):
        self.operation = '+'
        super().__init__(int_length, float_length, difficulty)

    def _generate_related_number(self) -> Number:
        if self.difficulty == Difficulty.EASY:
            max_digits_int = 1 if self.int_length == 1 else self.int_length - 1
            sum_limit = 1
        elif self.difficulty == Difficulty.MEDIUM:
            max_digits_int = self.int_length
            sum_limit = max(1, self.int_length - 1)
        elif self.difficulty == Difficulty.HARD:
            max_digits_int = min(self.int_length + 2, 18)  # Maximum 18 due to float precision
            sum_limit = max(3, min(self.int_length, 15))  # Maximum 15 due to float precision

        # Generate integer part.
        int_digits_count = randint(1, max_digits_int)
        num2 = Number(int_length=int_digits_count, float_length=self.float_length)

        n_above_limit = 0
        for i in range(int_digits_count):
            digit1 = self._num1.get_integer_digit(i) if i < self._num1.integer_length else 0
            max_digit2 = 9 if n_above_limit < sum_limit else 10 - 1 - digit1
            value = randint(0, max_digit2)
            if value + digit1 > 10: n_above_limit += 1
            num2.set_integer_digit(value, i)

        max_digits_float = self.float_length
        float_digits_count = randint(0, max_digits_float)
        for i in range(float_digits_count):
            digit1 = self._num1.get_float_digit(i) if i < self._num1.float_length else 0
            num2.set_float_digit(randint(0, 10 - 1 - digit1), i)

        return num2


class SubtractionQuiz(Quiz):
    def __init__(self, int_length: int, float_length: int, difficulty: Difficulty):
        self.operation = '-'
        super().__init__(int_length, float_length, difficulty)

    def _generate_related_number(self) -> Number:

        has_big_digit = False

        if self.difficulty == Difficulty.EASY:
            max_digits_int = 1 if self.int_length == 1 else self.int_length - 1
            limit = 1
        elif self.difficulty == Difficulty.MEDIUM:
            max_digits_int = self.int_length
            limit = max(1, self.int_length - 1)

            # Ensure at least one of the digits is greater than 5
            has_big_digit = False
        elif self.difficulty == Difficulty.HARD:
            max_digits_int = min(self.int_length + 2, 18)  # Maximum 18 due to float precision
            limit = max(3, min(self.int_length, 15))  # Maximum 15 due to float precision

        # Generate integer part.
        int_digits_count = randint(1, max_digits_int)
        num2 = Number(int_length=int_digits_count, float_length=self.float_length)

        for i in range(int_digits_count):
            digit1 = self._num1.get_integer_digit(i) if i < self._num1.integer_length else 0
            min_digit2 = 5 if not has_big_digit and i == int_digits_count - 1 else 0
            value = randint(min_digit2, 9)
            if self.difficulty == Difficulty.MEDIUM:
                if value > 5:
                    has_big_digit = True
            num2.set_integer_digit(value, i)

        max_digits_float = self.float_length
        float_digits_count = randint(0, max_digits_float)
        for i in range(float_digits_count):
            digit1 = self._num1.get_float_digit(i) if i < self._num1.float_length else 0
            min_digit2 = 5 if not has_big_digit else 0
            value = randint(min_digit2, 9)
            if self.difficulty == Difficulty.MEDIUM:
                if value > 5:
                    has_big_digit = True
            num2.set_float_digit(value, i)

        return num2

class MultiplicationQuiz(Quiz):
    def __init__(self, int_length: int, float_length: int, difficulty: Difficulty):
        self.operation = '*'
        super().__init__(int_length, float_length, difficulty)

    def _generate_related_number(self):
        return self._generate_number()


class DivisionQuiz(Quiz):
    def __init__(self, int_length: int, float_length: int, difficulty: Difficulty):
        self.operation = '/'
        super().__init__(int_length, float_length, difficulty)

    def _generate_related_number(self):
        # Generate a number strictly smaller than num1, for division to be less than 1
        max_value = min(self._num1.value, 10 ** self.int_length - 1)
        int_part = randint(1, int(max_value))
        float_part = randint(10 ** (self.float_length - 1),
                                    10 ** self.float_length - 1) / 10 ** self.float_length
        return Number(int_part + float_part)
