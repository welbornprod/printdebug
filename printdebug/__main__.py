#!/usr/bin/env python3
""" PrintDebug
    ...Just a small test implementation for printdebug.
    -Christopher Welborn 08-21-2014
"""
import sys
from __init__ import printdebug


def main():
    printdebug('Hello from main().')
    another_func()
    return 0


def another_func():
    def a_nested_func():
        printdebug('Hello from a nested function.')
    a_nested_func()
    printdebug('Hello from another_func.')

if __name__ == '__main__':
    sys.exit(main())
