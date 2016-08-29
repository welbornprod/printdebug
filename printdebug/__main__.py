#!/usr/bin/env python3
""" PrintDebug
    ...Just a small test implementation for printdebug.
    -Christopher Welborn 08-21-2014
"""
import sys
import printdebug as pd
from printdebug import __version__, get_lineinfo, debug


def main():
    pd.debug('Hello from main().')
    debug('The old functions still work.')
    return run_tests(
        another_func_test,
        debugprinter_test,
        disable_test,
        lineinfo_str_test,
        color_format_test,
        level_test,
        continued_test,
        align_test,
    )


def align_test():
    """ debug(align=True) should align content without the lineinfo. """
    debug('Next line will be aligned with this one.')
    debug('...so is it?', align=True)
    dp = pd.DebugPrinter()
    dp.debug('DebugPrinter, next line will be aligned.')
    dp.debug('...is it aligned?', align=True)

    try:
        cp = pd.DebugColrPrinter()
    except ImportError:
        return 0
    cp.debug('DebugColrPrinter, next line will be aligned.')
    cp.debug('...was it aligned?', align=True)
    return 0


def another_func_test():
    """ Function names are reported correctly, even when nested in another.
    """
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
        cp = pd.DebugColrPrinter(basename=True)
    except ImportError as ex:
        print(
            'Unable to test color formatting, no colr module:\n{}'.format(ex)
        )
        return 1
    cp.debug('Testing DebugColrPrinter.')

    def sub_function():
        cp.debug('using the default ljustwidth.')
    sub_function()
    return 0


def continued_test():
    """ Check auto-line-continuation. """
    # Intermingling these on purpose.
    debug('Starting on stderr', end='')
    debug('Starting on stdout', end='', file=sys.stdout)
    debug(', and continuing.')
    debug(', and continuing on stdout.', file=sys.stdout)
    debug('A separate stderr line.')
    debug('A separate stdout line.', file=sys.stdout)
    dp = pd.DebugPrinter()
    dp.debug('DebugPrinter, starting on stderr', end='')
    dp.debug('DebugPrinter, starting on stdout', end='', file=sys.stdout)
    dp.debug(', and continuing.')
    dp.debug(', and continuing.', file=sys.stdout)
    try:
        cp = pd.DebugColrPrinter()
    except ImportError:
        return 0
    cp.debug('DebugColrPrinter, starting on stderr', end='')
    cp.debug('DebugColrrinter, starting on stdout', end='', file=sys.stdout)
    cp.debug(', and continuing.')
    cp.debug(', and continuing.', file=sys.stdout)

    return 0


def debugprinter_test():
    """ Debug printer uses it's config to format the line info. """
    dp = pd.DebugPrinter(
        fmt='{filename}.{lineno}>{name}: ',
        ljustwidth=60,
        basename=False)
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


def level_test():
    """ Walk backwards through the frame levels. """
    try:
        dp = pd.DebugColrPrinter()
    except ImportError as ex:
        # If this is because colr is not installed, ignore it.
        if ex.name != 'colr':
            raise
        dp = pd.DebugPrinter()

    def sub_function():
        def subsub_function():
            for i in range(0, 10):
                try:
                    info = get_lineinfo(level=i)
                except ValueError:
                    break
                dp.debug(''.join((' ' * (10 - i), info.name)))
        subsub_function()
    sub_function()
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
    if ('-v' in sys.argv) or ('--version' in sys.argv):
        print('printdebug v. {}'.format(__version__))
        sys.exit(0)

    sys.exit(main())
