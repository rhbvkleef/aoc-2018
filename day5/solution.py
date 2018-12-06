# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
from functools import partial

from bases import Day


class Solution(Day):
    examples_1 = [("dabAcCaCBAcCcaDA", 10)]
    examples_2 = [("dabAcCaCBAcCcaDA", 4)]

    @staticmethod
    def remove(data, character):
        num_removed = 0
        char_history = []
        for i in data:
            if i.lower() == chr(ord('a') + character):
                num_removed += 1
            elif len(char_history) > 0 and i.swapcase() == char_history[-1]:
                char_history.pop()
                num_removed += 2
            else:
                char_history.append(i)

        return len(data) - num_removed

    def part1(self, istest=False):
        return Solution.remove(self.data, -40)

    def part2(self, istest=False):
        return min(map(partial(Solution.remove, self.data), range(0, 26)))
