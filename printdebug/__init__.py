""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""

from .tools import (
    __version__,
    DebugColrPrinter,
    DebugNotEnabled,
    DebugPrinter,
    debug,
    debug_enable,
    debug_exc,
    debug_json,
    debug_object,
    default_colr_format,
    default_format,
    get_frame,
    get_lineinfo,
    json_str,
    object_str,
    pop_or,
    print_json,
    printobject,
    print_object,
    LineInfo,
    suppress,
)

from .catchers import (
    StdErrCatcher,
    StdOutCatcher,
)

__all__ = [
    '__version__',
    # Exported tools
    'DebugColrPrinter',
    'DebugNotEnabled',
    'DebugPrinter',
    'debug',
    'debug_enable',
    'debug_exc',
    'debug_json',
    'debug_object',
    'default_colr_format',
    'default_format',
    'get_frame',
    'get_lineinfo',
    'print_json',
    'print_object',
    'printobject',
    'LineInfo',
    # Exported extras
    'json_str',
    'object_str',
    'pop_or',
    'suppress',
    'StdErrCatcher',
    'StdOutCatcher',
]
