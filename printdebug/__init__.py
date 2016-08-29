""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""
from __future__ import print_function
from collections import namedtuple
from warnings import warn
import inspect
import os.path
import sys

try:
    from colr import (
        auto_disable as colr_auto_disable,
        Colr as C,
    )
    colr_auto_disable()
except ImportError:
    C = None

__version__ = '0.2.0'

__all__ = [
    'DebugPrinter',
    'debug',
    'debug_enable',
    'printdebug',
    'printobject',
    'LineInfo'
]

# Holds information about where the debug print came from.
LineInfo = namedtuple('LineInfo', ['filename', 'name', 'lineno'])

default_format = '{filename}:{lineno:>5} {name:>25}(): '
if C is None:
    default_colr_format = None
else:
    default_colr_format = C('').join(
        C('{filename}:', fore='yellow'),
        C('{lineno:>5} ', fore='blue'),
        C('{name:>25}', fore='magenta'),
        C('(): '),
    )


def LineInfo__str__(self):
    """ String representation for LineInfo tuple. """
    return default_format.format(
        filename=self.filename,
        name=self.name,
        lineno=self.lineno
    )
# Override default string repr for namedtuple LineInfo.
# This is a bit of a hack, but probably still better than another class.
LineInfo.__str__ = LineInfo__str__

# Module-level flag to disable debug() and DebugPrinter().debug().
# Better called through debug_enable(True/False)
_enabled = True


def debug_enable(enabled=True):
    """ Re-enable the debug function (if it was disabled).
        Disable it if enabled=False.
    """
    global _enabled
    _enabled = enabled


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
        if frame is None:
            raise ValueError('`level` is too large, there is no frame.')
        frame = frame.f_back
        level -= 1
    if frame is None:
        raise ValueError('`level` is too large, there is no frame.')

    return LineInfo(
        frame.f_code.co_filename,
        frame.f_code.co_name,
        frame.f_lineno)


def debug(*args, **kwargs):
    """ Wrapper for print() that adds file, line, and func info.
        Possibly raises a ValueError if the `level` argument is too large,
        and there is no frame at the desired level.

        Arguments:
            same as print()

        Keyword Arguments:
            same as print()
            ..also:
                parent       : Parent class to include name for methods.
                level        : Number of frames to go back.
                               Default: 1
                back         : Alias for `level`, will be deprecated soon.
                fmt          : .format() string for line info.
                               Default: '{filename}:{lineno} {name}(): '
                ljustwidth   : str.ljust() value for line info.
                               Default: 40
                basename     : Whether to use just the base name of the file.
                               Default: False
    """
    if not (_enabled and args):
        return None

    # Include parent class name when given.
    parent = pop_or(kwargs, 'parent')

    # Go back more than once when given.
    backlevel = pop_or(kwargs, 'level', 1)

    # Get format string.
    fmt = pop_or(kwargs, 'fmt', default_format)

    # Get ljust level.
    ljustwidth = pop_or(kwargs, 'ljustwidth', 40)

    info = get_lineinfo(level=backlevel)
    usebasename = pop_or(kwargs, 'basename', True)
    fname = os.path.split(info.filename)[-1] if usebasename else info.filename

    if parent:
        func = '{}.{}'.format(parent.__class__.__name__, info.name)
    else:
        func = info.name

    # Patch args to stay compatible with print().
    pargs = list(args)
    infostr = fmt.format(
        filename=fname,
        lineno=info.lineno,
        name=func).ljust(ljustwidth)
    text = kwargs.get('sep', ' ').join((str(s) for s in pargs))
    line = ''.join((str(infostr), text))
    print(line, **kwargs)


def pop_or(dct, key, default=None):
    """ Like dict.get, except it pops the key afterwards. """
    val = default
    with suppress(KeyError):
        val = dct.pop(key)
    return val


def printobject(obj, file=None, indent=0):
    """ Print a verbose representation of an object.
        The format depends on what kind of object it is.
        Tuples, Lists, and Dicts are recursively formatted according to the
        other rules below.
        Strings will be printed as is.
        Any other type will be printed using str() (Actually '{}'.format(obj))
        Arguments:
            obj    : Object to print.
            file     : Open file object, defaults to sys.stdout.
            indent : Internal use.
                     Can be used to set initial indention though.
                     Must be an integer. Default: 0
    """
    if file is None:
        file = sys.stdout

    if not hasattr(file, 'write'):
        errfmt = 'file must have a "write" method. Got: {} ({!r})'
        raise TypeError(errfmt.format(type(file), file))

    if isinstance(obj, dict):
        try:
            objkeys = sorted(obj.keys())
        except TypeError:
            # Mixed key types.
            objkeys = obj.keys()

        for k in objkeys:
            v = obj[k]
            print('{}{}:'.format(' ' * indent, k), file=file)
            if isinstance(v, dict):
                printobject(v, file=file, indent=indent + 4)
            elif isinstance(v, (list, tuple)):
                printobject(v, file=file, indent=indent + 4)
            else:
                print('{}{}'.format(' ' * (indent + 4), v), file=file)
    elif isinstance(obj, (list, tuple)):
        try:
            objitems = sorted(obj)
        except TypeError:
            # Mixed list/tuple
            objitems = obj

        for itm in objitems:
            if isinstance(itm, (list, tuple)):
                printobject(itm, file=file, indent=indent + 4)
            else:
                print('{}{}'.format(' ' * indent, itm), file=file)
    else:
        print('{}{}'.format(' ' * indent, obj), file=file)


class DebugPrinter(object):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """

    def __init__(self, fmt=None, ljustwidth=40, basename=True):
        self.fmt = fmt or default_format
        self.ljustwidth = ljustwidth
        self.basename = basename

    def debug(self, *args, **kwargs):
        """ Wrapper for print() that adds file, line, and func info. """
        if not (_enabled and args):
            return None
        # Include parent class name when given.
        parent = kwargs.get('parent', None)

        # Go back more than once when given.
        backlevel = kwargs.get('level', 1)

        info = get_lineinfo(level=backlevel)
        if self.basename:
            fname = os.path.split(info.filename)[-1]
        else:
            fname = info.filename

        if parent:
            func = '{}.{}'.format(parent.__class__.__name__, info.name)
        else:
            func = info.name

        # Patch args to stay compatible with print().
        pargs = list(args)
        infostr = self.fmt.format(
            filename=fname,
            lineno=info.lineno,
            name=func).ljust(self.ljustwidth)
        text = str(self.transform_text(
            kwargs.get('sep', ' ').join((str(s) for s in pargs))
        ))

        # infostr may be a Colr instance.
        line = ''.join((str(infostr), text))

        # Pop all kwargs for this function. Send the rest to print().
        with suppress(KeyError):
            kwargs.pop('back')
        with suppress(KeyError):
            kwargs.pop('level')
        with suppress(KeyError):
            kwargs.pop('parent')

        print(line, **kwargs)

    def transform_text(self, text):
        """ Run a transformation on the actual text before printing. """
        # This is meaningless for DebugPrinter, and a little bit of a hack
        # to make DebugColrPrinter work without reimplementing debug().
        return str(text)


class DebugColrPrinter(DebugPrinter):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """
    textcolor = 'green'

    def __init__(self, fmt=None, ljustwidth=40, basename=True):
        if default_colr_format is None:
            imperr = ImportError(
                'colr is not installed, you can install it with pip.'
            )
            imperr.name = 'colr'
            raise imperr

        super(DebugColrPrinter, self).__init__(
            fmt=fmt or default_colr_format,
            ljustwidth=ljustwidth,
            basename=basename,
        )

    def transform_text(self, text):
        """ Transform all debug text, colorizing it. """
        return C(text, fore=self.textcolor)


class suppress:
    """Context manager to suppress specified exceptions

    * Borrowed from contextlib.py to cut down on imports and use with py2.

    After the exception is suppressed, execution proceeds with the next
    statement following the with statement.

         with suppress(FileNotFoundError):
             os.remove(somefile)
         # Execution still resumes here if the file was already removed
    """

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        # Unlike isinstance and issubclass, CPython exception handling
        # currently only looks at the concrete type hierarchy (ignoring
        # the instance and subclass checking hooks). While Guido considers
        # that a bug rather than a feature, it's a fairly hard one to fix
        # due to various internal implementation details. suppress provides
        # the simpler issubclass based semantics, rather than trying to
        # exactly reproduce the limitations of the CPython interpreter.
        #
        # See http://bugs.python.org/issue12029 for more details
        return exctype is not None and issubclass(exctype, self._exceptions)


# Save an alias to the debug function for backwards compatibility,
printdebug = debug
