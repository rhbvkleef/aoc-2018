# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
from collections import defaultdict, Counter

import datetime
import re

from bases import Day


class Solution(Day):
    examples_1 = [("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""", 240)]
    examples_2 = [("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""", 4455)]

    def accumulate(self):
        lines = re.compile(r'\[(?P<date>[0-9\- :]+)\] (?P<message>[0-9a-zA-Z #]+)')
        beginShift = re.compile(r'Guard #(?P<id>[0-9]+) begins shift')
        guards = defaultdict(list)
        guard = -1
        start = 0
        for line in sorted([lines.search(line).groups() for line in self.data.splitlines()], key=lambda d: d[0]):
            if line[1] == "falls asleep":
                start = datetime.datetime.strptime(line[0], '%Y-%m-%d %H:%M')
            elif line[1] == "wakes up":
                guards[int(guard)].extend([(start + datetime.timedelta(minutes=x)).minute for x in range(0, int((datetime.datetime.strptime(line[0], '%Y-%m-%d %H:%M') - start).total_seconds() / 60))])
            else:
                guard = int(beginShift.search(line[1]).group('id'))
        return guards

    def part1(self):
        guards = self.accumulate()

        m = max(guards.items(), key=lambda g: len(g[1]))

        return m[0] * max(set(m[1]), key=m[1].count)

    def part2(self):
        guards = self.accumulate()

        guard = max(map(lambda it: (it[0], max(Counter(it[1]).items(), key=lambda a: a[1])), guards.items()), key=lambda a: a[1][1])

        return guard[0] * guard[1][0]
