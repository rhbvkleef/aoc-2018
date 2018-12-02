# Advent of code 2018 in Python

[![License](https://img.shields.io/github/license/rhbvkleef/aoc-2018.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
![GitHub top language](https://img.shields.io/github/languages/top/rhbvkleef/aoc-2018.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg)
[![Python 3..6.6](https://img.shields.io/badge/python-3.6.6-blue.svg?logo=python)](https://www.python.org/downloads/release/python-366/)
[![Pipenv](https://img.shields.io/badge/pipenv-%E2%9C%94-brightgreen.svg)](https://pipenv.readthedocs.io/en/latest/)

## How to use

This project defines a few commands:

### new ([int]|"all")?

Creates a template for the given days, all days, or, when no day is specified,
the current day.

It also automatically downloads the required puzzle input and wires it to your
code as a string input in `self.data`.

### run ([int(.int)?]|"all")?

Runs the code for the given days, all days, or, when no day is specified, the
current day.

It is also possible to specify specific parts of each day to be run.

Examples:

* `./manage.py run` Runs both parts for today
* `./manage.py run 5.1` Only runs the first part of day 5
* `./manage.py run all` Runs all parts of all days

### test ([int(.int)?]|"all")?

Runs the unittests for the given days, all days, or, when no day is specified,
the current day.

It is also possible to specify specific parts of each day to be run.

Examples:

* `./manage.py test` Runs both parts for today
* `./manage.py test 5.1` Only runs the first part of day 5
* `./manage.py test all` Runs all parts of all days

### auto ([int(.int)?]|"all")?

Runs new for each given day, when no template exists. If that is not the case,
it will run unittests, and if they are successful, runs the actual input.

## License

[LGPLv2.1](LICENSE)