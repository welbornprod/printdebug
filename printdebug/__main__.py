#!/usr/bin/env python3
""" PrintDebug
    ...Just a small test implementation for printdebug.
    -Christopher Welborn 08-21-2014
"""
from __future__ import print_function
import sys

from .tools import (
    __version__,
    get_lineinfo,
    debug,
    debug_enable,
    debug_exc,
    debug_json,
    debug_object,
    DebugColrPrinter,
    DebugPrinter,
    printobject,
)

if sys.version_info.major < 3:
    print('Color printing is not available in Python 2.\n\n', file=sys.stderr)
    DebugColrPrinter = DebugPrinter  # noqa


def main(nameargs):
    if not nameargs:
        debug('Hello from main().')
        debug('The old functions still work.')
        return run_tests(
            align_test,
            another_func_test,
            color_format_test,
            continued_test,
            debug_err_test,
            debug_exc_test,
            debug_json_test,
            debug_object_test,
            debugprinter_test,
            disable_instance_test,
            disable_test,
            level_test,
            lineinfo_str_test,
            printobject_test,
        )
    # Run tests by name.
    test_funcs = []
    globs = globals()
    for test_name in test_names:
        for name in nameargs:
            if name in test_name:
                test_funcs.append(globs[test_name])
    if not test_funcs:
        print(
            '\nNo test functions found with: {}'.format(
                ', '.join(nameargs)
            ),
            file=sys.stderr,
        )
        return 1
    return run_tests(*test_funcs)


def align_test():
    """ debug(align=True) should align content without the lineinfo. """
    debug('Next line will be aligned with this one.')
    debug('...so is it?', align=True)
    dp = DebugPrinter()
    dp.debug('DebugPrinter, next line will be aligned.')
    dp.debug('...is it aligned?', align=True)

    try:
        cp = DebugColrPrinter()
    except ImportError as ex:
        print(ex, file=sys.stderr)
        return 0
    cp.debug('DebugColrPrinter, next line will be aligned.')
    cp.debug('...was it aligned?', align=True)
    return 0


def another_func_test():
    """ Function names are reported correctly, even when nested in another.
    """
    def a_nested_func_test():
        debug('Hello from a nested function.')
        debug('Should show from another_func_test.', level=2)
        return 0

    debug(
        'Testing format from another_func_test.',
        fmt='{name}, #{lineno} in {filename}: ')
    return 0 + a_nested_func_test()


def color_format_test():
    """ Try using the fmt argument to add colors using the colr module. """
    try:
        cp = DebugColrPrinter(basename=True)
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
    dp = DebugPrinter()
    dp.debug('DebugPrinter, starting on stderr', end='')
    dp.debug('DebugPrinter, starting on stdout', end='', file=sys.stdout)
    dp.debug(', and continuing.')
    dp.debug(', and continuing.', file=sys.stdout)
    try:
        cp = DebugColrPrinter()
    except ImportError:
        return 0
    cp.debug('DebugColrPrinter, starting on stderr', end='')
    cp.debug('DebugColrrinter, starting on stdout', end='', file=sys.stdout)
    cp.debug(', and continuing.')
    cp.debug(', and continuing.', file=sys.stdout)

    return 0


def debug_err_test():
    """ Debug_err should use the correct color. """
    cp = DebugColrPrinter()
    if not hasattr(cp, 'debug_err'):
        debug('No DebugColrPrinter available.')
    cp.debug_err('This error message should be a different color.')


def debug_exc_test():
    """ Debug_exc should show the correct caller. """
    try:
        raise FileNotFoundError('just a test')
    except FileNotFoundError:
        debug_exc('From function:')

    try:
        raise FileNotFoundError('just a test')
    except FileNotFoundError:
        DebugColrPrinter().debug_exc('From debugprinter:')


def debug_json_test():
    """ Debug json should show the correct caller. """
    x = {'a': [1, 2, 3], 'b': (5, 6, 7)}
    debug_json(x)
    DebugColrPrinter().debug_json(x)


def debug_object_test():
    """ Debug object should show the correct caller. """
    x = {'a': [1, 2, 3], 'b': (5, 6, 7)}
    debug_object(x)
    DebugColrPrinter().debug_object(x)


def debugprinter_test():
    """ Debug printer uses it's config to format the line info. """
    dp = DebugPrinter(
        fmt='{filename}.{lineno}>{name}: ',
        ljustwidth=60,
        basename=False)
    dp.debug('Testing DebugPrinter with ljustwidth = 60.')
    return 0


def disable_test():
    """ debug_enable(False) should silence output from debug() and
        DebugPrinter.debug().
    """
    debug('Disabling debug.')
    debug_enable(False)
    for i in range(5):
        debug('{} If you can read this something is wrong.'.format(
            i))
    DebugPrinter().debug('DebugPrinter should not print this.')
    debug_enable()
    debug('Debug re-enabled.')
    return 0


def disable_instance_test():
    """ debugprinter.disable() should disable a single instance, while leaving
        the others untouched.
    """
    dp, dp2 = DebugColrPrinter(), DebugColrPrinter()
    dp.debug('Disabling this instance.')
    dp.disable()
    dp2.debug('The first DebugPrinter was disabled.')
    dp.debug('This should not print.')
    dp.enable()
    dp.debug('DebugPrinter re-enabled.')
    return 0


def level_test():
    """ Walk backwards through the frame levels. """
    try:
        dp = DebugColrPrinter()
    except ImportError as ex:
        # If this is because colr is not installed, ignore it.
        if ex.name != 'colr':
            raise
        dp = DebugPrinter()

    def sub_function():
        def subsub_function():
            for i in range(0, 6):
                try:
                    info = get_lineinfo(level=i)
                except ValueError:
                    break
                dp.debug(''.join((' ' * (10 - i), info.name)), level=i)
        subsub_function()
    sub_function()
    return 0


def lineinfo_str_test():
    """ get_lineinfo() returns a LineInfo, and str(LineInfo()) works. """
    l = get_lineinfo()
    print('{} --> Testing LineInfo__str__'.format(l))
    return 0


def printobject_test():
    """ printobject() correctly nests dict, iterable keys/values. """
    o = {'test': {'child': {'subchild': [1, 2, 3]}, 'child2': ('a', 1, None)}}
    print('\nTesting printobject({!r}):'.format(o))
    printobject(o, indent=4)
    return 0


def run_tests(*funcs):
    """ Print a header for each function, and then call it. """
    testlen = len(funcs)
    if testlen == len(test_names):
        testlen = 'all'
    print('\nRunning {} test {}...'.format(
        testlen,
        'function' if testlen == 1 else 'functions',
    ))
    errs = 0
    for func in funcs:
        print('\nTesting with {}:'.format(func.__name__))
        errs += func() or 0

    print('\nFinished running {} test {}. (errors: {})'.format(
        testlen,
        'function' if testlen == 1 else 'functions',
        errs,
    ))
    return errs


test_names = sorted(s for s in dir() if s.endswith('_test'))


if __name__ == '__main__':
    if ('-h' in sys.argv) or ('--help' in sys.argv):
        print("""
    Usage: printdebug [TEST_NAME]
           printdebug [-l]

    Options:
        TEST_NAME  : Text/Regex pattern for test functions to run.
        -h,--help  : Show this message and exit.
        -l,--list  : Show test function names and exit.
        -v,--version  : Show printdebug version and exit.
        """)
        sys.exit(0)
    if ('-v' in sys.argv) or ('--version' in sys.argv):
        print('printdebug v. {}'.format(__version__))
        sys.exit(0)
    if ('-l' in sys.argv) or ('--list' in sys.argv):
        print('Test functions: ({})\n    {}'.format(
            len(test_names),
            '\n    '.join(test_names)
        ))
        sys.exit(0)

    sys.exit(main(sys.argv[1:]))
