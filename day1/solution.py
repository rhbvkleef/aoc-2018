# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.

from bases import Day


class Solution(Day):
    examples_1 = [
        ('\n'.join("+1, +1, +1".split(', ')), 3),
        ('\n'.join("+1, +1, -2".split(', ')), 0),
        ('\n'.join("-1, -2, -3".split(', ')), -6),
    ]
    examples_2 = [
        ('\n'.join("+1, -1".split(', ')), 0),
        ('\n'.join("+3, +3, +4, -2, -4".split(', ')), 10),
        ('\n'.join("-6, +3, +8, +5, -6".split(', ')), 5),
        ('\n'.join("+7, +7, -2, -7, -4".split(', ')), 14),
    ]

    def part1(self, istest=False):
        return sum(map(int, self.data.splitlines()))

    def part2(self, istest=False):
        data = list(map(int, self.data.splitlines()))

        results = set()
        v = 0
        results.add(0)

        while True:
            for s in data:
                v += s
                if v in results:
                    return v
                results.add(v)
