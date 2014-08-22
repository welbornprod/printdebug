""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""
from __future__ import print_function
from collections import namedtuple
import inspect

__version__ = '0.0.2'

# Holds information about where the debug print came from.
LineInfo = namedtuple('LineInfo', ['filename', 'name', 'lineno'])


def LineInfo__str__(self):
    """ String representation for LineInfo tuple. """
    return ' '.join([
        '{}'.format(self.filename),
        'line #{}'.format(self.lineno),
        'in {}:'.format(self.name),
    ])
# Override default string repr for namedtuple LineInfo.
LineInfo.__str__ = LineInfo__str__


def get_lineinfo(level=0):
    """ Gets information about the current line.
        If level is given, we will go back some frames.
        This is because we usually want to know where thing() was called,
        not where get_lineinfo() was called.
    """
    try:
        level = abs(level)
    except TypeError:
        level = 0

    frame = inspect.currentframe()
    # Go back some number of frames if needed.
    while level > -1:
        frame = frame.f_back
        level -= 1

    return LineInfo(
        frame.f_code.co_filename,
        frame.f_code.co_name,
        frame.f_lineno)


def printdebug(*args, **kwargs):
    """ Print a debug line.
        Arguments:
            same as print().

        Example:
            printdebug('Hey.')
        Output:
            ./myfile.py line #2 in my_function: Hey.
    """
    # Get line info from wherever printdebug was called.
    lineinfo = get_lineinfo(level=1)
    # New debug formatted line.
    debugstr = ' '.join((str(lineinfo), ' '.join(args)))
    print(debugstr, **kwargs)
