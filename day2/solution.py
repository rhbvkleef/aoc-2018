import itertools

from collections import Counter

import functools
import operator

from bases import Day


class Solution(Day):
    examples_1 = [(
        """abcdef
        bababc
        abbcde
        abcccd
        aabcdd
        abcdee
        ababab""", 12
    )]
    examples_2 = [(
        """abcde
        fghij
        klmno
        pqrst
        fguij
        axcye
        wvxyz""", "fgij"
    )]

    def part1(self):
        return functools.reduce(
            operator.mul,
            map(sum, zip(*[
                (1 if 2 in letters.values() else 0, 1 if 3 in letters.values() else 0)
                for current in self.data.splitlines()
                for letters in [Counter(current)]])))

    def part2(self):
        for a, b in itertools.combinations(map(str.strip, self.data.splitlines()), 2):
            intersect = [x for i, x in enumerate(b) if x == a[i]]
            if len(a) - len(intersect) == 1:
                return "".join(intersect)
