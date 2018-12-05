# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
from bases import Day


class Solution(Day):
    examples_1 = [("dabAcCaCBAcCcaDA", 10)]
    examples_2 = [("dabAcCaCBAcCcaDA", 4)]

    @staticmethod
    def remove(data, character):
        curr_len = len(data)
        curr_chars = []
        for i in data:
            if i.lower() == chr(ord('a') + character):
                curr_len -= 1
            elif len(curr_chars) > 0 and i.isupper() and i.lower() == curr_chars[-1]:
                curr_chars.pop()
                curr_len -= 2
            elif len(curr_chars) > 0 and i.islower() and i.upper() == curr_chars[-1]:
                curr_chars.pop()
                curr_len -= 2
            else:
                curr_chars.append(i)

        return curr_len

    def part1(self):
        return Solution.remove(self.data, -40)

    def part2(self):
        data = self.data
        best = len(data)

        for c in range(0, 26):
            best = min(Solution.remove(self.data, c), best)

        return best
