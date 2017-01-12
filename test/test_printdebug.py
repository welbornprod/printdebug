#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test_printdebug.py
    Unit tests for printdebug.py.

    -Christopher Welborn 01-11-2017
"""

import sys
import unittest

from printdebug import (
    __version__,
    debug,
    default_format,
    DebugPrinter,
    DebugColrPrinter,
    get_frame,
    get_lineinfo,
    LineInfo,
    StdErrCatcher,
)

print('Testing PrintDebug v. {}'.format(__version__), file=sys.stderr)
class HelperTests(unittest.TestCase):

    def test_get_frame(self):
        """ get_frame should return the proper frame. """
        f = get_frame()
        self.assertEqual(
            'test_get_frame',
            f.f_code.co_name,
            msg='Failed to get correct frame.'
        )

        def nested_function():
            return get_frame()
        self.assertEqual(
            'nested_function',
            nested_function().f_code.co_name,
            msg='Failed to get correct frame for nested function.'
        )

    def test_get_lineinfo(self):
        """ get_lineinfo should return the proper function names. """
        li = get_lineinfo()
        self.assertEqual(
            'test_get_lineinfo',
            li.name,
            msg='Failed to get correct function-level info.'
        )

        def nested_function():
            return get_lineinfo()
        self.assertEqual(
            'nested_function',
            nested_function().name,
            msg='Failed to get correct nested-function-level info.'
        )


class LineInfoTests(unittest.TestCase):

    def test_LineInfo_from_frame(self):
        """ LineInfo.from_frame should create a valid LineInfo. """
        li = LineInfo.from_frame(get_frame())
        self.assertEqual(
            'test_LineInfo_from_frame',
            li.name,
            msg='Failed to get correct LineInfo from function level.'
        )

        def nested_function():
            return LineInfo.from_frame(get_frame())

        self.assertEqual(
            'nested_function',
            nested_function().name,
            msg='Failed to get correct LineInfo from function level.'
        )

    def test_LineInfo_from_level(self):
        """ LineInfo.from_level should create a valid LineInfo. """
        li = LineInfo.from_level(0)
        self.assertEqual(
            'test_LineInfo_from_level',
            li.name,
            msg='Failed to get correct LineInfo from function level.'
        )

        def nested_function():
            return LineInfo.from_level(0)

        self.assertEqual(
            'nested_function',
            nested_function().name,
            msg='Failed to get correct LineInfo from function level.'
        )


class DebugTests(unittest.TestCase):
    """ Tests for the module-level `debug` function. """
    def test_debug_funcname(self):
        """ debug outputs the correct function name. """
        with StdErrCatcher() as err:
            # Passing `file` explicitly because of green test-runners.
            # They don't play nicely with my own catchers.
            # Tell `debug` to output to whatever sys.stderr is at the time
            # of this method's compilation (a green StringIO catcher).
            debug('Test.', file=sys.stderr)
        self.assertIn(
            'test_debug_funcname',
            err.output,
            msg='Failed to output correct function name.',
        )
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to output correct text.',
        )

        def nested_function():
            debug('NestedTest.', file=sys.stderr)
        with StdErrCatcher() as nestederr:
            nested_function()
        self.assertIn(
            'nested_function',
            nestederr.output,
            msg='Failed to output correct function name for nested function.',
        )
        self.assertIn(
            'NestedTest.',
            nestederr.output,
            msg='Failed to output correct text for nested function.',
        )


class DebugPrinterTests(unittest.TestCase):
    """ Tests for the module-level `debug` function. """
    def test_DebugPrinter_disable(self):
        """ DebugPrinter._enabled is set by all the properties/methods. """
        dp = DebugPrinter(fmt=default_format)
        dp.disabled = False
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to enable debugprinter with disabled=False.'
        )

        dp.disabled = True
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertEqual(
            '',
            err.output,
            msg='Failed to disable debugprinter with disabled=True.'
        )

        dp.enabled = True
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to enable debugprinter with enabled=True.'
        )

        dp.enabled = False
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertEqual(
            '',
            err.output,
            msg='Failed to disable debugprinter with enabled=False.'
        )

        dp.enable()
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to enable debugprinter with enabled().'
        )

        dp.disable()
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertEqual(
            '',
            err.output,
            msg='Failed to disable debugprinter with disable().'
        )

    def test_DebugPrinter_funcname(self):
        """ debug outputs the correct function name. """
        dp = DebugPrinter(fmt=default_format)
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertIn(
            'test_DebugPrinter_funcname',
            err.output,
            msg='Failed to output correct function name.',
        )
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to output correct text.',
        )

        def nested_function():
            dp = DebugPrinter()
            dp.debug('NestedTest.', file=sys.stderr)

        with StdErrCatcher() as nestederr:
            nested_function()

        self.assertIn(
            'nested_function',
            nestederr.output,
            msg='Failed to output correct nested function name.',
        )
        self.assertIn(
            'NestedTest.',
            nestederr.output,
            msg='Failed to output correct text for nested function.',
        )


if __name__ == '__main__':
    sys.exit(unittest.main(argv=sys.argv))
