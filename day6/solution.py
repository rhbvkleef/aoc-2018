# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
from collections import defaultdict

from bases import Day

import itertools


def partial(func, *args, **keywords):
    """
    Had to add this replacement partial implementation because
    python's standard one is shit.
    :param func:
    :param args:
    :param keywords:
    :return:
    """
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(newfunc.leftmost_args + fargs + newfunc.rightmost_args), **newkeywords)

    newfunc.func = func
    args = iter(args)
    newfunc.leftmost_args = tuple(itertools.takewhile(lambda v: v != Ellipsis, args))
    newfunc.rightmost_args = tuple(args)
    newfunc.keywords = keywords
    return newfunc


class Solution(Day):
    examples_1 = [("""1, 1
                  1, 6
                  8, 3
                  3, 4
                  5, 5
                  8, 9""", 17)]
    examples_2 = [("""1, 1
                  1, 6
                  8, 3
                  3, 4
                  5, 5
                  8, 9""", 16)]

    def part1(self, istest=False):
        self.points = list(map(
            lambda x: (int(x[0]), int(x[1])),
            map(
                partial(str.split, ..., ', '),
                map(
                    str.strip,
                    self.data.splitlines()
                )
            )
        ))

        maxx = max(self.points, key=lambda x: x[0])[0]
        maxy = max(self.points, key=lambda x: x[1])[1]

        self.grid = [[0] * (maxy + 1) for x in range(maxx + 1)]
        regions = defaultdict(int)

        for x in range(maxx + 1):
            for y in range(maxy + 1):
                best = maxx + maxy
                best_group = -1

                for i, point in enumerate(self.points):
                    dist = abs(x - point[0]) + abs(y - point[1])

                    if dist < best:
                        best = dist
                        best_group = i
                    elif dist == best:
                        best_group = -1

                self.grid[x][y] = best_group
                regions[best_group] += 1

        for line in self.grid:
            if line[0] in regions:
                regions.pop(line[0])
            if line[-1] in regions:
                regions.pop(line[-1])

        for x in range(maxx):
            if self.grid[0][x] in regions:
                regions.pop(self.grid[0][x])
            if self.grid[-1][x] in regions:
                regions.pop(self.grid[-1][x])

        return max(regions.items(), key=lambda x: x[1])[1]

    def part2(self, istest=False):
        self.part1()
        maxdist = 32 if istest else 10_000

        size = 0

        for x, line in enumerate(self.grid):
            for y, slot in enumerate(line):
                if sum(map(lambda p: abs(x - p[0]) + abs(y - p[1]), self.points)) < maxdist:
                    size += 1

        return size
