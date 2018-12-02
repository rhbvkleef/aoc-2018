#!/usr/sbin/python3
import os
import sys

import unittest

import importlib
import requests
import timeit
from distutils.dir_util import copy_tree
from io import StringIO

import traceback
from typing import Tuple, Union, List

import config
from bases import Day, DayTest


def is_day_created(day):
    try:
        importlib.import_module("day{}.solution".format(day))
    except ModuleNotFoundError:
        return False
    return True


def load(day: int, load_data: bool = True) -> Union[bool, Day]:
    try:
        return importlib.import_module("day{}.solution".format(day))\
            .Solution(load_data=load_data)
    except ModuleNotFoundError:
        return False


def parse(args):
    if len(args) == 0:
        import datetime
        args = str(datetime.date.today().day)

    if args[0] == 'all':
        r = {}
        for day in range(1, 26):
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
    solution = load(day)

    if not solution:
        if notfound_errors:
            print("Day {}:".format(day))
            print("  Not found!")
        return False
    else:
        print("Day {}:".format(day))

    def run_case(func):
        try:
            start = timeit.default_timer()
            result = func()
            end = timeit.default_timer()
        except Exception as e:
            print("    Raised exception: {}".format(e))
            buffer = StringIO()
            traceback.print_exc(file=buffer)
            print("      " + ("\n      ".join(buffer.getvalue().split("\n"))))
        else:
            print("    Solution: {}".format(result))
            print("    Duration: {} ms".format((end-start) * 1000))

    if 1 in puzzles:
        print("  Part 1:")
        run_case(solution.part1)

    if 2 in puzzles:
        print("  Part 2:")
        run_case(solution.part2)

    return True


def new(day: int, show_error=True):
    cwd = os.path.dirname(__file__)
    src = os.path.join(cwd, "day_template")
    dst = os.path.join(cwd, "day{}".format(day))

    if os.path.isdir(dst):
        if show_error:
            print("Day {} already created!".format(day))
        return False

    r = requests.get(config.URL.format(day),
                     allow_redirects=True, cookies={'session': config.SESSION})

    if not r.ok:
        raise ConnectionError("Failed to download new input file. Status {}."
                              .format(r.status_code))

    copy_tree(src, dst)
    open(os.path.join(dst, "input.txt"), 'wb').write(r.content)

    print("Created template for day {}".format(day))

    return True


def get_tests(day: int, puzzles: Tuple[int, int] = (1, 2))\
        -> List[unittest.TestCase]:
    solution = load(day, load_data=False)

    tests = []
    for p in puzzles:
        tests.append(DayTest('test_part{}'.format(p), solution=solution))

    return tests


def run_tests(tests):
    runner = unittest.TextTestRunner(stream=sys.stdout)
    suite = unittest.TestSuite()

    for day, puzzles in tests.items():
        suite.addTests(get_tests(day, puzzles))

    return runner.run(suite).wasSuccessful()


def main():
    if len(sys.argv) < 2:
        exit(1)

    if sys.argv[1] in ('run-or-create', 'run-or-new',
                       'execute-or-create', 'execute-or-new', 'auto'):
        for day, puzzles in parse(sys.argv[2:]).items():
            if is_day_created(day):
                if run_tests({day: puzzles}):
                    run(day, puzzles)
            else:
                # noinspection PyBroadException
                try:
                    new(day)
                except ConnectionError as e:
                    print(e, file=sys.stderr)
                except Exception:
                    traceback.print_exc()
        exit(0)

    if sys.argv[1] in ('run', 'execute'):
        for day, puzzles in parse(sys.argv[2:]).items():
            run(day, puzzles)
    elif sys.argv[1] in ('new', 'create'):
        for day, puzzles in parse(sys.argv[2:]).items():
            new(day)
    elif sys.argv[1] in ('test', ):
        run_tests(parse(sys.argv[2:]))
    else:
        print('Valid commands are: (run|execute) and (new|create)')


if __name__ == '__main__':
    main()
