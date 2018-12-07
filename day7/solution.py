# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
from collections import defaultdict

import re

from bases import Day


class Solution(Day):
    examples_1 = [("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""", "CABDFE")]
    examples_2 = [("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""", 15)]

    def part1(self, istest=False):
        rx = re.compile(r'Step (?P<dependency>[A-Z]+) must be finished before step (?P<dependent>[A-Z]+) can begin.')
        deps = defaultdict(lambda: {'dependents': [], 'dependencies': []})

        for dependent, dependency in map(lambda l: rx.findall(l)[0], self.data.splitlines()):
            deps[dependent]['dependencies'].append(dependency)
            deps[dependency]['dependents'].append(dependent)

        order = ""

        while len(deps) > 0:
            d = sorted([dep for dep in deps.items() if len(dep[1]['dependents']) == 0], key=lambda i: i[0])[0]
            for dep in d[1]['dependencies']:
                deps[dep]['dependents'].remove(d[0])
            del deps[d[0]]
            order += d[0]

        return order

    def part2(self, istest=False):
        if istest:
            workers = 2
            d_fun = lambda c: ord(c) - ord('A') + 1
        else:
            workers = 5
            d_fun = lambda c: ord(c) - ord('A') + 61

        rx = re.compile(r'Step (?P<dependency>[A-Z]+) must be finished before step (?P<dependent>[A-Z]+) can begin.')
        deps = defaultdict(lambda: {'dependents': [], 'dependencies': []})

        for dependent, dependency in map(lambda l: rx.findall(l)[0], self.data.splitlines()):
            deps[dependent]['dependencies'].append(dependency)
            deps[dependency]['dependents'].append(dependent)

        order = ""

        current = (0, [])
        jobs = defaultdict(list)
        jobs[0] = {'dependencies': [], 'dependents': []}

        while len(current[1]) > 0 or current[0] == 0:
            current = min(jobs.items())
            for job in current[1]['dependencies']:
                for dep in job[1]:
                    deps[dep]['dependents'].remove(job[0])
                workers += 1

            available = [dep for dep in deps.items() if len(dep[1]['dependents']) == 0][::]
            while workers > 0 and len(available) > 0:
                d = sorted(available, key=lambda i: -ord(i[0]))[0]
                print(d)
                available.remove(d)
                del deps[d[0]]
                jobs[d_fun(d[0]) + current[0]] += d
                workers -= 1

            del jobs[current[0]]

        return current[0]
