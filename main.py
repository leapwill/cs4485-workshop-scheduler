#!/usr/bin/env python3

from .objects import MusicClass, ElectiveClass
from . import csv
import asyncio
import sys
if sys.version_info < (3, 7):
    print('Please update to Python 3.7 or newer.')
    exit(37)


async def main():
    print('Hello, world!')
    import_csv()

if __name__ == "__main__":
    if sys.version_info >= (3, 7):
        asyncio.run(main())

# https://docs.python.org/3/tutorial/modules.html

# https://www.python.org/dev/peps/pep-0008/#imports
