#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class StdOutCatcher(object):

    """ Catches stdout for code inside the 'with' block.

        Usage:
            with StdOutCatcher(safe=True, maxlength=160) as fakestdout:
                # stdout is stored in fakestdout.output
                print('okay')
            # stdout is back to normal
            # retrieve the captured output..
            print('output was: {}'.format(fakestdout.output))
    """

    def __init__(self, safe=False, maxlength=160):
        # Use safe_output?
        self.safe = safe
        # Maximum length before trimming output
        self.maxlength = maxlength
        # Output
        self.lines = []

    def __enter__(self):
        # Replace stdout with self, stdout.write() will be self.write()
        self.oldstdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exctype, value, traceback):
        # Fix stdout.
        sys.stdout = self.oldstdout
        # Allow exceptions to propogate by not returning True.
        return None

    @property
    def output(self):
        return '\n'.join(self.lines)

    @output.setter
    def output(self, value):
        self.lines = value.split('\n')

    def safe_output(self, s):
        """ Escape output and check max length, trim if needed. """

        s = repr(s)[1:-1]
        if self.maxlength and (len(s) > self.maxlength):
            s = '{} (..truncated)'.format(s[:self.maxlength])
        return s

    def write(self, s):
        s = s.strip('\n')
        if not s:
            return 0
        # Save output
        self.lines.append(self.safe_output(s) if self.safe else s)
        return len(s)


class StdErrCatcher(StdOutCatcher):

    def __enter__(self):
        # Replace stderr with self, stdout.write() will be self.write()
        self.oldstderr = sys.stderr
        sys.stderr = self
        return self

    def __exit__(self, exctype, value, traceback):
        # Fix stdout.
        sys.stderr = self.oldstderr
        # Allow exceptions to propogate by not returning True.
        return None
