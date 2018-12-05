#!/usr/sbin/python3

# Copyright 2018 Rolf van Kleef
# This library is licensed under the BSD 3-clause license. This means that you
# are allowed to do almost anything with it. For exact terms, please refer to
# the attached license file.
import datetime
import os
import sys

import unittest

import importlib
import re
import requests
import timeit
from distutils.dir_util import copy_tree
from io import StringIO

import traceback
from typing import Tuple, Union, List

from teamcity.unittestpy import TeamcityTestRunner, TeamcityTestResult

import config
from bases import Day, DayTest

use_teamcity = 'TEAMCITY' in os.environ
TestRunner = TeamcityTestRunner if use_teamcity else unittest.TextTestRunner


class TextTestResultWithSuccesses(TeamcityTestResult if use_teamcity else unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TextTestResultWithSuccesses, self).__init__(*args, **kwargs)
        self.successes = []
    def addSuccess(self, test):
        super(TextTestResultWithSuccesses, self).addSuccess(test)
        self.successes.append(test)


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
        args = str(datetime.date.today().day)

    if args[0] == 'all':
        r = {}
        for day in range(1, 26):
            r[day] = (1, 2)
        return r
    else:
        days = {}
        for d in args:
            split = d.split('.')
            if len(split) == 1:
                days[int(split[0])] = (1, 2)
            elif len(split) == 2:
                days[int(split[0])] = days.get(int(split[0]), ()) + (int(split[1]), )
        return days


def run(day: int, puzzles: Tuple[int, int] = (1, 2), notfound_errors=True):
    solution = load(day)

    if not solution:
        if notfound_errors:
            print("Day {}:".format(day), file=sys.stderr)
            print("  Not found!", file=sys.stderr)
        return False
    else:
        print("Day {}:".format(day), file=sys.stderr)

    def run_case(func):
        try:
            start = timeit.default_timer()
            result = func()
            end = timeit.default_timer()
        except Exception as e:
            print("    Raised exception: {}".format(e), file=sys.stderr)
            buffer = StringIO()
            traceback.print_exc(file=buffer)
            print("      " + ("\n      ".join(buffer.getvalue().split("\n"))), file=sys.stderr)
        else:
            print("    Solution: {}".format(result), file=sys.stderr)
            print("    Duration: {} ms".format((end-start) * 1000), file=sys.stderr)

    if 1 in puzzles:
        print("  Part 1:", file=sys.stderr)
        run_case(solution.part1)

    if 2 in puzzles:
        print("  Part 2:", file=sys.stderr)
        run_case(solution.part2)

    return True


def new(day: int, show_error=True):
    cwd = os.path.dirname(__file__)
    src = os.path.join(cwd, "template")
    dst = os.path.join(cwd, "day{}".format(day))

    if os.path.isdir(dst):
        if show_error:
            print("Day {} already created!".format(day), file=sys.stderr)
        return False

    s = requests.Session()
    s.cookies.update({'session': config.SESSION})
    s.headers.update({
        'X-Email': 'aoc@rolfvankleef.nl',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) rhbvkleef/aoc-2018',
    })

    r = s.get(config.URL.format(day), allow_redirects=True)

    if not r.ok:
        raise ConnectionError("Failed to download new input file. Status {}."
                              .format(r.status_code))

    copy_tree(src, dst)
    open(os.path.join(dst, "input.txt"), 'wb').write(r.content)

    print("Created template for day {}".format(day), file=sys.stderr)

    return True


def get_tests(day: int, puzzles: Tuple[int, int] = (1, 2))\
        -> List[unittest.TestCase]:
    solution = load(day, load_data=False)

    tests = []
    for p in (1, 2):
        if solution:
            tests.append(DayTest.new(day, solution, p, puzzles))
        else:
            tests.append(DayTest.new(day, solution, p, ()))

    return tests


def run_tests(tests):
    # noinspection PyTypeChecker
    runner = TestRunner(stream=sys.stdout,
                        resultclass=TextTestResultWithSuccesses)
    suite = unittest.TestSuite()

    for day in range(1, 26):
        suite.addTests(get_tests(day, tests.get(day, ())))

    result = runner.run(suite)

    passed = {}

    # noinspection PyUnresolvedReferences
    for test in result.successes:
        a = int(re.match(r'day([0-9]+).solution', test.solution.__module__)
                .group(1))

        # noinspection PyProtectedMember
        if '1' in test._testMethodName:
            passed[a] = passed.get(a, ()) + (1,)
        elif '2' in test._testMethodName:
            passed[a] = passed.get(a, ()) + (2,)

    return passed


def main():
    if sys.argv[0] in ('manage', 'manage.py'):
        sys.argv.pop(0)

    if sys.argv[0] in ('run-or-create', 'run-or-new',
                       'execute-or-create', 'execute-or-new', 'auto'):
        should_execute = {int(day): puzzles
                          for day, puzzles in parse(sys.argv[1:]).items()
                          if is_day_created(day)}
        should_create = [day for day, _ in parse(sys.argv[1:]).items()
                         if not is_day_created(day)]

        for day in should_create:
            # noinspection PyBroadException
            try:
                new(day)
            except ConnectionError as e:
                print(e, file=sys.stderr)
            except Exception:
                traceback.print_exc()

        passes = run_tests(should_execute)
        for day, puzzles in passes.items():
            run(day, puzzles)

        return

    if sys.argv[0] in ('run', 'execute'):
        for day, puzzles in parse(sys.argv[1:]).items():
            run(day, puzzles)
    elif sys.argv[0] in ('new', 'create'):
        for day, puzzles in parse(sys.argv[1:]).items():
            new(day)
    elif sys.argv[0] in ('test', ):
        run_tests(parse(sys.argv[1:]))
    else:
        print('Valid commands are: (run|execute) and (new|create)', file=sys.stderr)
        print('You entered "{}"'.format(' '.join(sys.argv[1:])), file=sys.stderr)


if __name__ == '__main__':
    main()


class FullTest(unittest.TestSuite):
    def __init__(self):
        super(FullTest, self).__init__(sum([get_tests(day, (1, 2))
                                            for day in range(1, 26)], []))


class TestToday(DayTest):
    def __init__(self, test_name):
        k, v = list(parse([]).items())[0]
        super(TestToday, self).__init__(test_name, load(k, load_data=False),
                                        puzzles=(1, 2))


class AutoToday(unittest.TestSuite):
    def __init__(self):
        self.day = datetime.date.today().day

        if not is_day_created(self.day):
            new(self.day)
            exit(0)

        super(AutoToday, self).__init__(tests=[
            TestToday(test_name='test_part1'),
            TestToday(test_name='test_part2'),
        ])

    def run(self, result, debug=False):
        super(AutoToday, self).run(result)

        passes = (1, 2)

        for failure in result.failures:
            if '1' in failure[0]._testMethodName:
                if passes == (1, 2):
                    passes = (2, )
                else:
                    passes = ()
            elif '2' in failure[0]._testMethodName:
                if passes == (1, 2):
                    passes = (1, )
                else:
                    passes = ()

        for skip in result.skipped:
            if '1' in skip[0]._testMethodName:
                if passes == (1, 2):
                    passes = (2, )
                else:
                    passes = ()
            elif '2' in skip[0]._testMethodName:
                if passes == (1, 2):
                    passes = (1, )
                else:
                    passes = ()
            pass

        print()
        run(self.day, passes)
        sys.stdout.flush()

        return result

