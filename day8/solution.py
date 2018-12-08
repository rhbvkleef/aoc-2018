# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.

from bases import Day


class Solution(Day):
    examples_1 = [("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2", 138)]
    examples_2 = [("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2", 66)]

    def part1(self, istest=False):
        nums = list(map(int, self.data.split()))

        nodes = []
        sum_meta = 0

        while True:
            while len(nodes) > 0 and nodes[-1][0] == 0:
                sum_meta += sum(nums[:nodes[-1][1]])
                nums = nums[nodes[-1][1]:]
                nodes.pop()

            if len(nums) == 0:
                break

            node_count = nums.pop(0)
            meta_count = nums.pop(0)

            if len(nodes) > 0:
                nodes[-1][0] -= 1

            nodes.append([node_count, meta_count])

        return sum_meta


    def part2(self, istest=False):
        nums = list(map(int, self.data.split()))

        root = {'meta': [], 'children': [], 'parent': None}
        current = root
        nodes = [[nums.pop(0), nums.pop(0)]]

        while True:
            while len(nodes) > 0 and nodes[-1][0] == 0:
                current['meta'] = nums[:nodes[-1][1]]
                nums = nums[nodes[-1][1]:]
                nodes.pop()
                current = current['parent']

            if len(nums) == 0:
                break

            node_count = nums.pop(0)
            meta_count = nums.pop(0)

            if len(nodes) > 0:
                nodes[-1][0] -= 1
                current['children'] += [{'meta': [], 'children': [], 'parent': current}]
                current = current['children'][-1]

            nodes.append([node_count, meta_count])

        return Solution.valueof(root)

    @staticmethod
    def valueof(node):
        if len(node['children']) == 0:
            return sum(node['meta'])

        chv = list(map(Solution.valueof, node['children']))

        return sum(map(lambda i: chv[i-1] if i <= len(chv) else 0, node['meta']))
