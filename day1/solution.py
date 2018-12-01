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

    def part1(self):
        return sum([int(v) for v in self.data.splitlines()])

    def part2(self):
        results = set()
        v = 0
        results.add(0)
        while True:
            for s in self.data.splitlines():
                v += int(s)
                if v in results:
                    return v
                results.add(v)
