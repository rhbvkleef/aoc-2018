import itertools

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
        counts2 = 0
        counts3 = 0
        for current in self.data.splitlines():
            letters = {}
            for letter in current:
                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1
            if 2 in letters.values():
                counts2 += 1
            if 3 in letters.values():
                counts3 += 1

        return counts2 * counts3

    def part2(self):
        """
        I found out that this program is able to produce multiple solutions for
        my given puzzle input. The one it currently returns first is different
        from the one I entered, so either I am making a mistake, or there are
        just multiple possible answers.

        :return: A solution
        """
        for a, b in itertools.combinations(map(str.strip, self.data.splitlines()), 2):
            set_a = frozenset(a)
            intersect = [x for x in b if x in set_a]
            if len(a) - len(intersect) == 1:
                return "".join(intersect)
