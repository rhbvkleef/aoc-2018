import os

from abc import ABC, abstractmethod
from unittest import TestCase

from typing import Tuple


class Day(ABC):

    data: str

    def __init__(self, load_data=True):
        if not load_data:
            return

        path = os.path.join(*type(self).__module__.split('.')[:-1])
        self.data = open("{}/input.txt".format(path), "r").read().strip()

    @abstractmethod
    def part1(self):
        pass

    @abstractmethod
    def part2(self):
        pass


class DayTest(TestCase):
    solution: Day
    puzzles: Tuple

    def __init__(self, testName, solution):
        super(DayTest, self).__init__(testName)
        self.solution = solution

    def test_part1(self):
        if not hasattr(self.solution, 'examples_1')\
                or len(self.solution.examples_1) == 0:
            self.fail('There are no tests for part 1')

        for input, answer in self.solution.examples_1:
            self.solution.data = input
            self.assertEqual(answer, self.solution.part1())

    def test_part2(self):
        if not hasattr(self.solution, 'examples_2')\
                or len(self.solution.examples_2) == 0:
            self.fail('There are no tests for part 2')

        for input, answer in self.solution.examples_2:
            self.solution.data = input
            self.assertEqual(answer, self.solution.part2())
