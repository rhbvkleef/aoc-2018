# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
import itertools

import collections

from bases import Day


class Solution(Day):
    examples_1 = [("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""", 4)]
    examples_2 = [("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""", 3)]

    def parse(self):
        squares = []
        for line in self.data.splitlines():
            s0 = line.split(': ')
            dim = tuple(map(int, s0[1].split('x')))
            pos = tuple(map(int, s0[0].split()[-1].split(',')))
            id = int(s0[0].split()[0][1:])
            squares.append((pos, dim, id))

        return squares

    @staticmethod
    def squares_intersect(square0, square1):
        min_x = max(square0[0][0], square1[0][0])
        min_y = max(square0[0][1], square1[0][1])
        max_x = min(square0[0][0]+square0[1][0], square1[0][0]+square1[1][0])
        max_y = min(square0[0][1]+square0[1][1], square1[0][1]+square1[1][1])

        if min_x > max_x or min_y > max_y:
            return []

        list1 = list(range(min_x, max_x))
        list2 = list(range(min_y, max_y))

        return list(itertools.product(list1, list2))

    def part1(self, istest=False):
        squares = self.parse()
        intersects = 0
        for i, square in enumerate(squares):
            s = itertools.chain.from_iterable([Solution.squares_intersect(square, sq) for sq in squares[:i]])
            ctr = collections.Counter(s)
            for item, count in ctr.items():
                if count == 1:
                    intersects = intersects + 1

        return intersects

    def part2(self, istest=False):
        squares = self.parse()
        for i, square in enumerate(squares):
            if sum(map(len, [Solution.squares_intersect(square, sq) for sq in squares if sq != square])) == 0:
                return square[2]
