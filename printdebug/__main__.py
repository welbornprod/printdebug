#!/usr/bin/env python3
""" PrintDebug
    ...Just a small test implementation for printdebug.
    -Christopher Welborn 08-21-2014
"""
import sys
import printdebug as pd
from printdebug import printdebug


def main():
    pd.debug('Hello from main().')
    printdebug('The old functions still work.')
    return run_tests(
        another_func_test,
        debugprinter_test,
        disable_test,
        lineinfo_str_test,
        color_format_test,
    )


def another_func_test():
    """ Function names are reported correctly, even when nested in another. """
    def a_nested_func_test():
        pd.debug('Hello from a nested function.')
        pd.debug('Should show from another_func_test.', level=2)
        return 0

    pd.debug(
        'Testing format from another_func_test.',
        fmt='{name}, #{lineno} in {filename}: ')
    return 0 + a_nested_func_test()


def color_format_test():
    """ Try using the fmt argument to add colors using the colr module. """
    try:
        from colr import Colr as C
    except ImportError as ex:
        print('Unable to test color formatting, no colr module:\n{}'.format(
            ex))
        return 1

    colrfmt = str(C('').join(
        C('{filename} ', 'blue'),
        C('#{lineno} ', 'cyan'),
        C('in '),
        C('{name}', 'magenta'),
        C(':'),
        C(' ', 'green')))
    pd.debug('Testing colors.', fmt=colrfmt)
    dp = pd.DebugPrinter(fmt=colrfmt, basename=True)
    dp.debug('Testing colors from DebugPrinter.')
    return 0


def debugprinter_test():
    """ Debug printer uses it's config to format the line info. """
    dp = pd.DebugPrinter(
        fmt='{filename}.{lineno}>{name}: ',
        ljustwidth=60,
        basename=True)
    dp.debug('Testing DebugPrinter with ljustwidth = 60.')
    return 0


def disable_test():
    """ debug_enable(False) should silence output from debug() and
        DebugPrinter.debug().
    """
    pd.debug('Disabling pd.debug.')
    pd.debug_enable(False)
    for i in range(5):
        pd.debug('{} If you can read this something is wrong.'.format(
            i))
    pd.DebugPrinter().debug('DebugPrinter should not print this.')
    pd.debug_enable()
    pd.debug('Debug re-enabled.')
    return 0


def lineinfo_str_test():
    """ get_lineinfo() returns a LineInfo, and str(LineInfo()) works. """
    l = pd.get_lineinfo()
    print('{} --> Testing LineInfo__str__'.format(l))
    return 0


def printobject_test():
    """ printobject() correctly nests dict, iterable keys/values. """
    o = {'test': {'child': {'subchild': [1, 2, 3]}, 'child2': ('a', 1, None)}}
    print('\nTesting printobject({!r}):'.format(o))
    pd.printobject(o, indent=4)
    return 0


def run_tests(*funcs):
    """ Print a header for each function, and then call it. """
    errs = 0
    for func in funcs:
        print('\nTesting with {}:'.format(func.__name__))
        errs += func()
    return errs


if __name__ == '__main__':
    sys.exit(main())
