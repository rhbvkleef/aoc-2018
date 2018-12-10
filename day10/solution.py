# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
import re

from bases import Day


class Solution(Day):
    examples_1 = [("""osition=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""", """
*   *  ***
*   *   * 
*   *   * 
*****   * 
*   *   * 
*   *   * 
*   *   * 
*   *  ** """)]
    examples_2 = [("""osition=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""", 3)]

    def common(self):
        rx = re.compile("position=<(?P<px>[ 0-9\\-]+),(?P<py>[ 0-9\\-]+)> velocity=<(?P<vx>[ 0-9\\-]+),(?P<vy>[ 0-9\\-]+)>")

        data = [{k: int(v) for k, v in i.groupdict().items()} for i in rx.finditer(self.data)]

        sizes = []

        for i in range(20000):
            minx = min(d['px'] + i * d['vx'] for d in data)
            miny = min(d['py'] + i * d['vy'] for d in data)
            maxx = max(d['px'] + i * d['vx'] for d in data)
            maxy = max(d['py'] + i * d['vy'] for d in data)

            sz = abs(maxx - minx) * abs(miny - maxy)
            sizes.append((sz, i))

        return min(sizes)[1], data

    def part1(self, istest=False):
        pos, data = self.common()

        message = [[' '] * 400 for i in range(400)]

        for d in data:
            message[d['py'] + pos * d['vy']][d['px'] + pos * d['vx'] + 200] = '*'

        ignores = []
        min_prefix = 400
        min_postfix = 0

        for i, l in enumerate(message):
            try:
                idx = l.index('*')
                min_prefix = min(min_prefix, idx)
                min_postfix = max(min_postfix, len(l) - l[::-1].index('*'))
            except ValueError:
                ignores.append(i)

        ignores_idx = 0
        result = ""

        for i, l in enumerate(message):
            if ignores_idx < len(ignores) and ignores[ignores_idx] == i:
                ignores_idx += 1
                continue
            result += "\n"
            result += ''.join(l[min_prefix:min_postfix])

        return result

    def part2(self, istest=False):
        pos, data = self.common()

        return pos
