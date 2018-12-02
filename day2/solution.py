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
        import itertools
        for a, b in itertools.combinations(map(str.strip, self.data.splitlines()), 2):
            ctr = 0
            res = ""
            for i, c in enumerate(a):
                if c != b[i]:
                    ctr += 1
                else:
                    res += c

                if ctr >= 2:
                    break

            if ctr == 0 or ctr >= 2:
                continue

            return res
