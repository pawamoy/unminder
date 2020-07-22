"""
Entry-point module, in case you use `python -m unminder`.

Why does this file exist, and why `__main__`? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

import sys

from unminder.cli import review

if __name__ == "__main__":
    sys.exit(review(sys.argv[1:]))
