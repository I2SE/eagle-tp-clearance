# eagle-tp-clearance
[![Build Status](https://travis-ci.org/I2SE/eagle-tp-clearance.py.svg)](https://travis-ci.org/I2SE/eagle-tp-clearance.py)

# usage
usage: eagle-tp-clearance.py [-h] [-l LIMIT] [--verbose] boardfile

Check eagle files for the distance between testpoints. The printed value is
the distance from center to center of the testpads.

positional arguments:
  boardfile

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        define a value that is used as test condition for the
                        minimum tp distance, a TP distance higher than the
                        limit results in an error
  --verbose, -v         show more information

