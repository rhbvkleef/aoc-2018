#!/usr/sbin/python3
import sys

import unittest
from typing import Tuple, Union, List

from bases import Day, DayTest


def load(day: int, load_data: bool = True) -> Union[bool, Day]:
    import importlib

    try:
        return importlib.import_module("day{}.solution".format(day)).Solution(load_data=load_data)
    except ModuleNotFoundError:
        return False


def parse(args):
    if len(args) == 0:
        import datetime
        args = str(datetime.date.today().day)

    if args[0] == 'all':
        import importlib
        r = {}
        for day in range(1, 26):
            try:
                importlib.import_module("day{}.solution".format(day))
            except ModuleNotFoundError:
                pass
            else:
                r[day] = (1, 2)
        return r
    else:
        days = {}
        for d in args:
            split = d.split('.')[0]
            if len(split) == 1:
                days[split[0]] = (1, 2)
            elif len(split) == 2:
                days[split[0]] = days[split[0]] + int(split[1])
        return days


def run(day: int, puzzles: Tuple[int, int] = (1, 2), notfound_errors=True):
    import timeit

    solution = load(day)

    if not solution:
        if notfound_errors:
            print("Day {}:".format(day))
            print("  Not found!")
        return False
    else:
        print("Day {}:".format(day))

    if 1 in puzzles:
        print("  Part 1:")
        start = timeit.default_timer()
        result = solution.part1()
        end = timeit.default_timer()
        print("    Solution: {}".format(result))
        print("    Duration: {}s".format(end-start))

    if 2 in puzzles:
        print("  Part 2:")
        start = timeit.default_timer()
        result = solution.part2()
        end = timeit.default_timer()
        print("    Solution: {}".format(result))
        print("    Duration: {}s".format(end-start))

    return True


def new(day: int, show_error=True):
    from distutils.dir_util import copy_tree
    import os
    import requests
    import config

    cwd = os.path.dirname(__file__)
    src = os.path.join(cwd, "day_template")
    dst = os.path.join(cwd, "day{}".format(day))

    if os.path.isdir(dst):
        if show_error:
            print("Day {} already created!".format(day))
        return False

    copy_tree(src, dst)

    r = requests.get(config.URL.format(day), allow_redirects=True, cookies={'session': config.SESSION})
    open(os.path.join(dst, "input.txt"), 'wb').write(r.content)

    print("Created template for day {}".format(day))

    return True


def get_tests(day: int, puzzles: Tuple[int, int] = (1, 2)) -> List[unittest.TestCase]:
    solution = load(day, load_data=False)

    tests = []
    for p in puzzles:
        tests.append(DayTest('test_part{}'.format(p), solution=solution))

    return tests


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)

    if sys.argv[1] in ('run-or-create', 'run-or-new', 'execute-or-create', 'execute-or-new', 'auto'):
        for day, puzzles in parse(sys.argv[2:]).items():
            if not run(day, puzzles, notfound_errors=False):
                new(day)
        exit(0)

    if sys.argv[1] in ('run', 'execute'):
        for day, puzzles in parse(sys.argv[2:]).items():
            run(day, puzzles)
    elif sys.argv[1] in ('new', 'create'):
        for day, puzzles in parse(sys.argv[2:]).items():
            new(day)
    elif sys.argv[1] in ('test', ):
        runner = unittest.TextTestRunner(stream=sys.stderr)
        suite = unittest.TestSuite()

        for day, puzzles in parse(sys.argv[2:]).items():
            suite.addTests(get_tests(day, puzzles))

        runner.run(suite)
    else:
        print('Valid commands are: (run|execute) and (new|create)')
