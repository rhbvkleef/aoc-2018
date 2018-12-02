# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.

import os

from abc import ABC, abstractmethod
from unittest import TestCase

from typing import Tuple, Any, List


class Day(ABC):

    data: str
    examples_1: List[Tuple[str, Any]]
    examples_2: List[Tuple[str, Any]]

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

    # noinspection PyPep8Naming
    def __init__(self, testName, solution, puzzles=(1, 2)):
        super(DayTest, self).__init__(testName)
        self.solution = solution
        self.not_skip = puzzles

    def test_part1(self):
        if 1 not in self.not_skip:
            self.skipTest('This test is not specified.')

        if not hasattr(self.solution, 'examples_1'):
            self.fail('There are no tests for part 1')

        for data, answer in self.solution.examples_1:
            self.solution.data = data
            self.assertEqual(answer, self.solution.part1())

    def test_part2(self):
        if 2 not in self.not_skip:
            self.skipTest('This test is not specified.')

        if not hasattr(self.solution, 'examples_2'):
            self.fail('There are no tests for part 2')

        for data, answer in self.solution.examples_2:
            self.solution.data = data
            self.assertEqual(answer, self.solution.part2())

    @staticmethod
    def new(day, solution, puzzle, puzzles):
        cls = type('{}'.format(day), (DayTest, ), {'__module__': 'days'})
        return cls('test_part{}'.format(puzzle), solution=solution,
                   puzzles=puzzles)
