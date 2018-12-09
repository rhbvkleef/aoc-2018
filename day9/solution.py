# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
import re
from blist._blist import blist

from bases import Day


class Solution(Day):
    examples_1 = [("9 players; last marble is worth 25 points", 32),
                  ("10 players; last marble is worth 1618 points", 8317),
                  ("13 players; last marble is worth 7999 points", 146373),
                  ("17 players; last marble is worth 1104 points", 2764),
                  ("21 players; last marble is worth 6111 points", 54718),
                  ("30 players; last marble is worth 5807 points", 37305)]
    examples_2 = [("9 players; last marble is worth 25 points", 22563)]

    @staticmethod
    def solve(data):
        line = blist()
        points = [0] * data.get('players')
        idx = 0
        plr = 0

        for i in range(0, data.get('points') + 1):
            if len(line) == 0:
                idx = 0
                line.insert(idx, i)
            else:
                if i % 23 == 0:
                    idx = ((idx - 8) % (len(line))) + 1
                    points[plr] += line.pop(idx) + i
                else:
                    idx = ((idx + 1) % (len(line))) + 1
                    line.insert(idx, i)
            plr = (plr + 1) % len(points)

        return max(points)

    def part1(self, istest=False):
        data = {k: int(v) for k, v in next(re.finditer(r'(?P<players>[0-9]+) players; last marble is worth (?P<points>[0-9]+) points', self.data)).groupdict().items()}
        return Solution.solve(data)

    def part2(self, istest=False):
        d = next(re.finditer(r'(?P<players>[0-9]+) players; last marble is worth (?P<points>[0-9]+) points', self.data)).groupdict()

        return Solution.solve({'players': int(d['players']), 'points': 100 * int(d['points'])})
