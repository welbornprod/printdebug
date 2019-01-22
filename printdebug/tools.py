""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""
from __future__ import print_function, with_statement

import inspect
import json
import os.path
import sys
import traceback
from warnings import warn

try:
    from colr import (
        auto_disable as colr_auto_disable,
        Colr as C,
    )
    colr_auto_disable()
except ImportError:
    C = None

__version__ = '0.3.5'

__all__ = [
    '__version__',
    'DebugColrPrinter',
    'DebugPrinter',
    'debug',
    'debug_enable',
    'debug_exc',
    'debug_json',
    'debug_object',
    'default_colr_format',
    'default_format',
    'enabled',
    'get_frame',
    'get_lineinfo',
    'json_str',
    'object_str',
    'pop_or',
    'print_json',
    'print_object',
    'printobject',
    'LineInfo',
    'suppress',
]

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

# Module-level flag to disable debug() and DebugPrinter().debug().
# Better called through debug_enable(True/False)
_enabled = True


def debug_enable(enabled=True):
    """ Re-enable the debug function (if it was disabled).
        Disable it if enabled=False.
    """
    global _enabled
    _enabled = enabled


def debug(*args, **kwargs):
    """ Wrapper for print() that adds file, line, and func info.
        Possibly raises a ValueError if the `level` argument is too large,
        and there is no frame at the desired level.

        Arguments:
            same as print()

        Keyword Arguments:
            same as print()
            ..also:
                align        : Omit the line info but use it's width as
                               indention.
                back         : Alias for `level`, will be deprecated soon.
                basename     : Whether to use just the base name of the file.
                               Default: False
                fmt          : .format() string for line info.
                               Default: printdebug.default_format
                level        : Number of frames to go back.
                               Default: 1
                ljustwidth   : str.ljust() value for line info.
                               Default: 40
                parent       : Parent class to include name for methods.
    """
    if not args:
        return None
    elif not _enabled:
        if debug.should_raise:
            raise DebugNotEnabled()
        return None

    # Use stderr by default.
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr

    # Include parent class name when given.
    parent = pop_or(kwargs, 'parent')

    # Go back more than once when given.
    backlevel = _ensure_level(pop_or(kwargs, 'level', 0))
    # Account for call to debug().
    backlevel += 1

    # Get format string.
    fmt = pop_or(kwargs, 'fmt', default_format)

    # Get ljust level.
    ljustwidth = pop_or(kwargs, 'ljustwidth', 40)

    # Are we omitting the line info, and just aligning with the end of it?
    align = pop_or(kwargs, 'align', False)

    info = get_lineinfo(level=backlevel)
    usebasename = pop_or(kwargs, 'basename', True)
    fname = os.path.split(info.filename)[-1] if usebasename else info.filename

    if parent:
        func = '{}.{}'.format(parent.__class__.__name__, info.name)
    else:
        func = info.name

    # Patch args to stay compatible with print().
    pargs = list(args)
    lineinfo = fmt.format(
        filename=fname,
        lineno=info.lineno,
        name=func).ljust(ljustwidth)

    # Is this a continuation from a previous line?
    # Getting this for debug(), re-setting for print().
    kwargs['end'] = kwargs.get('end', '\n')
    willcontinue = (not kwargs['end'].endswith('\n'))
    continued = debug.continued.get(kwargs['file'], False)
    if align or continued:
        debug.continued[kwargs['file']] = willcontinue
        if align:
            pargs[0] = ''.join((' ' * len(lineinfo), pargs[0]))
        print(*pargs, **kwargs)
        return None
    debug.continued[kwargs['file']] = willcontinue

    text = kwargs.get('sep', ' ').join((str(s) for s in pargs))
    line = ''.join((str(lineinfo), text))
    print(line, **kwargs)


# This dict keeps track of whether a line is "continued", based on the last
# `end` parameter, and it does so for each file descriptor used.
debug.continued = {sys.stderr: False}
# Whether debug() should raise DebugNotEnabled() when called while disabled.
debug.should_raise = False


def debug_exc(msg=None, suppress=None, suppress_strs=None):
    """ Print a formatted traceback for the last exception, if there is any.
        Arguments:
            msg            : Optional message to print before the traceback.
            suppress       : An iterable of exceptions to ignore.
                             If the last exception type is found in `suppress`
                             it will not be debug-printed.
            suppress_strs  : An iterable of strings. If str(last_exception)
                             contains any of these strings, it will not be
                             debug-printed.
    """
    if not _enabled:
        # No debugging exceptions when debug is disabled.
        return None
    # Show actual exception tracebacks.
    ex_type, ex_value, ex_tb = sys.exc_info()
    if suppress and (ex_type in suppress):
        # Ignore this exception type.
        return None
    elif suppress_strs:
        if str_contains(str(ex_value), suppress_strs):
            # Exception message matched a substring, don't debug it.
            return None
    if any((ex_type, ex_value, ex_tb)):
        if msg:
            debug(msg, level=1)
        debug(
            ''.join(
                traceback.format_exception(ex_type, ex_value, ex_tb)
            ),
            level=1,
        )


def debug_json(
        obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None, default=None,
        sort_keys=None, file=None, **kw):
    """ Debug-print a json object, like `print_json` does.
        This function uses sort_keys=True, and indent=4 by default.
    """
    debug(
        '\n{}'.format(json_str(
            obj=obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw,
        )),
        file=file,
        level=1,
    )


def debug_object(obj, file=None, indent=4):
    """ Debug-print an object like `print_object` does. """
    linegen = object_str(obj, indent=indent)
    firstline = linegen.send(None)
    debug(firstline, file=file, level=1)
    for line in linegen:
        debug(line, align=True, file=file, level=1)


def enabled():
    """ Access to global _enabled value. """
    return _enabled


def _ensure_level(level=0):
    """ Ensure the level argument is a non-negative integer, defaulting to 0
        on errors.
    """
    try:
        l = abs(level)
    except TypeError:
        return 0
    return l


def get_frame(level=0):
    """ Gets a previous frame for inspecting or getting source code info from.
    """
    level = _ensure_level(level)

    frame = inspect.currentframe()
    # Go back some number of frames if needed.
    while level > -1:
        if frame is None:
            raise ValueError('`level` is too large, there is no frame.')
        frame = frame.f_back
        level -= 1
    if frame is None:
        raise ValueError('`level` is too large, there is no frame.')
    return frame


def get_lineinfo(level=0):
    """ Gets information about the current line.
        If level is given, we will go back some frames.
        This is because we usually want to know where thing() was called,
        not where get_lineinfo() was called.
    """
    # Account for get_lineinfo() itself.
    return LineInfo.from_frame(get_frame(level=level + 1))


def json_str(
        obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None, default=None,
        sort_keys=None, **kw):
    """ Shortcut to json.dumps(obj, *args, **kwargs)
        This function uses sort_keys=True, and indent=4 by default.
    """
    if indent is None:
        indent = 4
    if sort_keys is None:
        # Saving the original arg value, so I can tell if the default
        # behavior may have actually caused problems.
        sortedkeys = True
    else:
        sortedkeys = sort_keys
    # I'm sorting keys by default, which may not go well.
    # If it fails, I'll try again without sorted keys.
    # If that fails, I'll raise the original error.
    try:
        s = json.dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sortedkeys,
            **kw
        )
    except TypeError as ex:
        if sort_keys:
            # Sorting keys by default didn't cause this error.
            # The user asked for them.
            raise
        # Try again without sorted keys (json.dumps default behavior)
        try:
            s = json.dumps(
                obj,
                skipkeys=skipkeys,
                ensure_ascii=ensure_ascii,
                check_circular=check_circular,
                allow_nan=allow_nan,
                cls=cls,
                indent=indent,
                separators=separators,
                default=default,
                sort_keys=False,
                **kw
            )
        except TypeError:
            # Raise the original error.
            raise ex
    return s


def object_str(obj, indent=0):
    """ Yield lines from a verbose representation of an object.
        The format depends on what kind of object it is.
        Tuples, Lists, and Dicts are recursively formatted according to the
        other rules below.
        Strings will be printed as is.
        Any other type will be printed using str() (Actually '{}'.format(obj))
        Arguments:
            obj      : Object to print.
            indent   : Internal use.
                       Can be used to set initial indention though.
                       Must be an integer. Default: 0
    """

    if isinstance(obj, str):
        yield '{}{}'.format(' ' * indent, obj)
    elif isinstance(obj, bytes):
        yield '{}{!r}'.format(' ' * indent, obj)
    elif isinstance(obj, dict):
        # Dict keys should be printed first, and then their values.
        try:
            keys = sorted(obj)
        except TypeError:
            # Not orderable.
            keys = list(obj)
        for key in keys:
            yield '{}{}:'.format(' ' * indent, str(key))
            yield from object_str(obj[key], indent=indent + 4)
    else:
        try:
            (_ for _ in obj)  # noqa
        except TypeError:
            # Not an iterable.
            yield '{}{}'.format(' ' * indent, str(obj))
        else:
            # Iterable.
            try:
                items = sorted(obj)
            except TypeError:
                # Not orderable.
                items = list(obj)
            for item in items:
                yield from object_str(item, indent=indent)


def pop_or(dct, key, default=None):
    """ Like dict.get, except it pops the key afterwards.
        This also works for lists and sets.
    """
    val = default
    with suppress(IndexError, KeyError, TypeError):
        val = dct.pop(key)
    return val


def print_json(
        obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None, default=None,
        sort_keys=None, file=None, **kw):
    """ Shortcut to print(json.dumps(obj, *args, **kwargs))
        This function uses sort_keys=True, and indent=4 by default.
    """
    print(
        json_str(
            obj=obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw,
        ),
        file=file or sys.stdout,
    )


def print_object(obj, file=None, indent=0):
    """ Print a verbose representation of an object.
        The format depends on what kind of object it is.
        Tuples, Lists, and Dicts are recursively formatted according to the
        other rules below.
        Strings will be printed as is.
        Any other type will be printed using str() (Actually '{}'.format(obj))
        Arguments:
            obj      : Object to print.
            file     : Open file object, defaults to sys.stdout.
            indent   : Internal use.
                       Can be used to set initial indention though.
                       Must be an integer. Default: 0
    """
    if file is None:
        file = sys.stdout

    if not hasattr(file, 'write'):
        errfmt = '`file` must have a `write` method. Got: {} ({!r})'
        raise TypeError(errfmt.format(type(file), file))

    for line in object_str(obj, indent=indent):
        print(line, file=file)


# TODO: printobject will be officially renamed soon.
def printobject(obj, file=None, indent=0):
    warn(
        '`printobject` is deprecated. Use `print_object` instead.',
        DeprecationWarning,
    )
    return print_object(obj, file=file, indent=indent)


def str_contains(s, substrs):
    """ Returns True if the str `s` contains any substrings in `substrs`.
        Like `substr in s`, except you can use an iterable of strings instead
        if just one.

        Arguments:
            s        : The string to search.
            substrs  : An iterable of substrings to find.
    """
    if isinstance(substrs, str):
        # Not supposed to pass a str in, but okay.
        return (substrs in s)
    try:
        return any((substr in s) for substr in substrs)
    except TypeError:
        raise ValueError(': '.join((
            'Expecting an iterable of `str` for `substr`, got',
            type(substrs).__name__,
        )))
    return False


class DebugNotEnabled(ValueError):
    """ Used with DebugOnly, to signal that code should not run. """
    pass


class DebugPrinter(object):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """
    def __init__(
            self, fmt=None, ljustwidth=40, basename=True, file=None,
            should_raise=False):
        self.fmt = fmt or default_format
        self.ljustwidth = ljustwidth
        self.basename = basename
        # Use stderr by default.
        self.file = file or sys.stderr
        # Keeps track of line continuations, per file descriptor.
        self.continued = {self.file: False}
        # Whether this single instance is disabled.
        self._enabled = True
        # Whether this instance should raise DebugNotEnabled, when debug()
        # is called while disabled.
        self.should_raise = should_raise

    def debug(self, *args, **kwargs):
        """ Wrapper for print() that adds file, line, and func info. """
        if not args:
            return None
        elif not (self._enabled and _enabled):
            if self.should_raise:
                raise DebugNotEnabled()
            return None
        # Use stderr by default.
        if kwargs.get('file', None) is None:
            kwargs['file'] = self.file

        # Include parent class name when given.
        parent = pop_or(kwargs, 'parent', None)

        # Go back more than once when given.
        backlevel = _ensure_level(pop_or(kwargs, 'level', 0))
        # Account for call to debug().
        backlevel += 1
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
        lineinfo = self.fmt.format(
            filename=fname,
            lineno=info.lineno,
            name=func).ljust(self.ljustwidth)
        # Run any transformations that child classes may have, or
        # any transformation functions that were passed in.
        transfunc = pop_or(kwargs, 'transform', self.transform_text)
        text = str(transfunc(
            kwargs.get('sep', ' ').join((str(s) for s in pargs)),
        ))

        align = pop_or(kwargs, 'align', False)
        # Is this a continuation from a previous line?
        # Getting this for debug(), re-setting for print().
        kwargs['end'] = kwargs.get('end', '\n')
        willcontinue = (not kwargs['end'].endswith('\n'))
        continued = self.continued.get(kwargs['file'], False)
        if align or continued:
            self.continued[kwargs['file']] = willcontinue
            if align:
                text = ''.join((' ' * self.lineinfo_len(lineinfo), text))
            print(text, **kwargs)
            return None
        self.continued[kwargs['file']] = willcontinue

        # lineinfo may be a Colr instance.
        line = ''.join((str(lineinfo), text))

        print(line, **kwargs)

    def debug_err(self, *args, **kwargs):
        """ Like `debug`, except the messages are passed through
            `self.transform_err` before printing.
        """
        kwargs['transform'] = kwargs.get('transform', self.transform_err)
        kwargs['level'] = kwargs.get('level', 0) + 1
        return self.debug(*args, **kwargs)

    def debug_exc(self, msg=None, suppress=None, suppress_strs=None):
        """ Print a formatted traceback for the last exception, if there is
            any.
            Arguments:
                msg            : Optional message to print before the
                                 traceback.
                suppress       : An iterable of exceptions to ignore.
                                 If the last exception type is found in
                                 `suppress` it will not be debug-printed.
                suppress_strs  : An iterable of strings.
                                 If str(last_exception) contains any of these
                                 strings, it will not be debug-printed.
        """
        if not _enabled:
            # No debugging exceptions when debug is disabled.
            return None
        # Show actual exception tracebacks.
        ex_type, ex_value, ex_tb = sys.exc_info()
        if suppress and (ex_type in suppress):
            # Ignore this exception type.
            return None
        elif suppress_strs:
            if str_contains(str(ex_value), suppress_strs):
                # Exception message matched a substring, don't debug it.
                return None
        if any((ex_type, ex_value, ex_tb)):
            if msg:
                self.debug(msg, level=1)
            self.debug(
                ''.join(
                    traceback.format_exception(ex_type, ex_value, ex_tb)
                ),
                level=1,
            )

    def debug_json(
            self, obj, skipkeys=False, ensure_ascii=True, check_circular=True,
            allow_nan=True, cls=None, indent=None, separators=None,
            default=None, sort_keys=None, file=None, **kw):
        """ Debug-print a json object, like `print_json` does.
            This function uses sort_keys=True, and indent=4 by default.
        """
        self.debug(
            '\n{}'.format(json_str(
                obj=obj,
                skipkeys=skipkeys,
                ensure_ascii=ensure_ascii,
                check_circular=check_circular,
                allow_nan=allow_nan,
                cls=cls,
                indent=indent,
                separators=separators,
                default=default,
                sort_keys=sort_keys,
                **kw,
            )),
            file=file,
            level=1,
        )

    def debug_object(self, obj, file=None, indent=4):
        """ Debug-print an object like `print_object` does. """
        linegen = object_str(obj, indent=indent)
        firstline = linegen.send(None)
        self.debug(firstline, file=file, level=1)
        for line in linegen:
            self.debug(line, align=True, file=file, level=1)

    def disable(self, disabled=True):
        """ Disable this instance. """
        self._enabled = not disabled

    @property
    def disabled(self):
        """ Dynamic property to query this debug printer's enabled/disabled
            value.
        """
        return not self._enabled

    @disabled.setter
    def disabled(self, value):
        self._enabled = not bool(value)

    def enable(self, enabled=True):
        """ Re-enable this instance, if it was disabled. """
        self._enabled = enabled

    @property
    def enabled(self):
        """ Dynamic property to query this debug printer's enabled/disabled
            value.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)

    def lineinfo_len(self, s):
        """ Overridable, returns the length of line info.
            This is needed in subclasses because of escape codes.
        """
        return len(s)

    def transform_err(self, text):
        """ Run a transformation on the actual text before printing,
            specifically for `debug_err`.
        """
        # This is meaningless for DebugPrinter. Derived classes may need
        # to transform the message text before printing.
        # This can be done by overriding 'self.transform_err', or passing
        # a `transform=my_function` to debug_err.
        return str(text)

    def transform_text(self, text):
        """ Run a transformation on the actual text before printing. """
        # This is meaningless for DebugPrinter. Derived classes may need
        # to transform the message text before printing.
        # This can be done by overriding 'self.transform_text', or passing
        # a `transform=my_function` to debug.
        return str(text)


class DebugColrPrinter(DebugPrinter):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """
    textcolor = 'green'
    errorcolor = 'red'

    def __init__(
            self, fmt=None, ljustwidth=40, basename=True, file=None,
            should_raise=False):
        if default_colr_format is None:
            # Raise an error on instantiation if colr is not available.
            # At least the Python 2 users can use the regular debug prints.
            if sys.version_info.major < 3:
                errmsg = '\n'.join((
                    'Color is not available in Python 2.',
                    'The colr module is required, but depends on Python 3+.'
                ))
            else:
                errmsg = '\n'.join((
                    'The colr module is required for DebugColrPrinter.',
                    '`colr` is not installed, you can install it with pip.',
                ))
            imperr = ImportError(errmsg)
            imperr.name = 'colr'
            raise imperr

        super(DebugColrPrinter, self).__init__(
            fmt=fmt or default_colr_format,
            ljustwidth=ljustwidth,
            basename=basename,
            file=file,
            should_raise=should_raise,
        )

    def lineinfo_len(self, s):
        """ Return a line length, without escape codes. """
        if hasattr(s, 'stripped'):
            return len(s.stripped())
        return len(s)

    def transform_err(self, text):
        """ Transform all debug error text, colorizing it. """
        return C(text, self.errorcolor)

    def transform_text(self, text):
        """ Transform all debug text, colorizing it. """
        return C(text, self.textcolor)


class LineInfo(object):
    """ Holds information about where the debug print came from. """
    def __init__(self, filename, name, lineno):
        self.filename = filename
        self.name = name
        self.lineno = lineno

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(k, getattr(self, k))
                for k in ('filename', 'lineno', 'name')
            )
        )

    def __str__(self):
        return default_format.format(
            filename=self.filename,
            name=self.name,
            lineno=self.lineno
        )

    @classmethod
    def from_frame(cls, frame):
        """ Construct a LineInfo from a frame, retrieved with `inspect`. """
        return cls(
            frame.f_code.co_filename,
            frame.f_code.co_name,
            frame.f_lineno
        )

    @classmethod
    def from_level(cls, level=0):
        level = _ensure_level(level)
        # Account for call to from_level.
        level += 1
        return cls.from_frame(get_frame(level=level))


class suppress:
    """Context manager to suppress specified exceptions

    * Borrowed from contextlib.py to use with py2.

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
        # See http://bugs.python.org/issue12029 for more details
        return (
            exctype is not None and issubclass(exctype, self._exceptions)
        )
