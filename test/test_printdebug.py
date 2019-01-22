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
    debug_exc,
    default_format,
    DebugPrinter,
    DebugColrPrinter,
    get_frame,
    get_lineinfo,
    json_str,
    LineInfo,
    object_str,
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
    """ Tests for the DebugPrinter class. """
    def setUp(self):
        self.dp_class = DebugPrinter
        self.class_name = self.dp_class.__name__

    def test_disable(self):
        """ DebugPrinter._enabled is set by all the properties/methods. """
        dp = self.dp_class(fmt=default_format)
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

    def test_funcname(self):
        """ debug outputs the correct function name. """
        dp = self.dp_class(fmt=default_format)
        with StdErrCatcher() as err:
            dp.debug('Test.', file=sys.stderr)
        self.assertIn(
            'test_funcname',
            err.output,
            msg='Failed to output correct function name.',
        )
        self.assertIn(
            'Test.',
            err.output,
            msg='Failed to output correct text.',
        )

        def nested_function():
            dp = self.dp_class(fmt=default_format)
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

    def test_debug_transform(self):
        """ debug_err uses transform_err. """
        def transform(text):
            return text.upper()

        dp = self.dp_class(fmt=default_format)
        with StdErrCatcher() as err:
            dp.debug('testing this', transform=transform, file=sys.stderr)
        self.assertIn(
            'TESTING THIS',
            err.output,
            msg='Failed to use transform_err function.',
        )

    def test_debug_err_transform(self):
        """ debug_err uses transform_err. """
        def transform(text):
            return text.upper()

        dp = self.dp_class(fmt=default_format)
        with StdErrCatcher() as err:
            dp.debug_err('testing this', transform=transform, file=sys.stderr)
        self.assertIn(
            'TESTING THIS',
            err.output,
            msg='Failed to use transform_err function.',
        )


class DebugColrPrinterTests(DebugPrinterTests):
    """ Tests for the DebugColrPrinter class. """
    def setUp(self):
        self.dp_class = DebugColrPrinter
        self.class_name = self.dp_class.__name__


class PrintTests(unittest.TestCase):
    def test_json_str(self):
        """ json_str should work with valid json. """
        obj = {
            'apple': [3, 1, 2],
            'diver': ('apricot', 'banana', 'cat'),
        }
        obj['f'] = obj.copy()
        obj['f']['f'] = obj['f'].copy()
        expected = """
{
    "apple": [
        3,
        1,
        2
    ],
    "diver": [
        "apricot",
        "banana",
        "cat"
    ],
    "f": {
        "apple": [
            3,
            1,
            2
        ],
        "diver": [
            "apricot",
            "banana",
            "cat"
        ],
        "f": {
            "apple": [
                3,
                1,
                2
            ],
            "diver": [
                "apricot",
                "banana",
                "cat"
            ]
        }
    }
}
"""
        self.assertEqual(
            json_str(obj).strip(),
            expected.strip(),
            msg='json_str output failed.'
        )

    def test_object_str(self):
        """ print_object should print all builtin types. """
        obj = {
            'apple': [3, 1, 2],
            'diver': ('apricot', 'banana', 'cat'),
            'extra': {3.3, 1.1, 2.2},
            'genius': b'ascii beef dead pi',
        }
        obj['f'] = obj.copy()
        obj['f']['f'] = obj['f'].copy()
        expected = """
apple:
    1
    2
    3
diver:
    apricot
    banana
    cat
extra:
    1.1
    2.2
    3.3
f:
    apple:
        1
        2
        3
    diver:
        apricot
        banana
        cat
    extra:
        1.1
        2.2
        3.3
    f:
        apple:
            1
            2
            3
        diver:
            apricot
            banana
            cat
        extra:
            1.1
            2.2
            3.3
        genius:
            b'ascii beef dead pi'
    genius:
        b'ascii beef dead pi'
genius:
    b'ascii beef dead pi'
"""
        self.assertEqual(
            '\n'.join(object_str(obj)).strip(),
            expected.strip(),
            msg='print_object output failed.'
        )


if __name__ == '__main__':
    sys.exit(unittest.main(argv=sys.argv))
