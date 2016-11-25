""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""

from .tools import (
    DebugColrPrinter,
    DebugNotEnabled,
    DebugPrinter,
    debug,
    debug_enable,
    printdebug,
    printobject,
    LineInfo,
    suppress,
)

from .catchers import (
    StdErrCatcher,
    StdOutCatcher,
)

__all__ = [
    # Exported tools
    'DebugColrPrinter',
    'DebugNotEnabled',
    'DebugPrinter',
    'debug',
    'debug_enable',
    'printdebug',
    'printobject',
    'LineInfo',
    # Exported extras
    'suppress',
    'StdErrCatcher',
    'StdOutCatcher',
]
