# eagle-tp-clearance
Check eagle files for the distance between testpoints. The returned value is
the distance from center to center of the testpads.

# usage
usage: eagle-tp-clearance.py [-h] [-l LIMIT] boardfile

Check eagle files for the distance between testpoints. The returned value is
the distance from center to center of the testpads.

positional arguments:
  boardfile

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        define a value that is used as test condition for the
                        minimum tp distance, a TP distance higher than the
                        limit results in an error
