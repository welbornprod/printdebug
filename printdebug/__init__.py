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
    default_colr_format,
    default_format,
    get_frame,
    get_lineinfo,
    printobject,
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
    'default_colr_format',
    'default_format',
    'get_frame',
    'get_lineinfo',
    'printobject',
    'LineInfo',
    # Exported extras
    'suppress',
    'StdErrCatcher',
    'StdOutCatcher',
]
