PrintDebug
==========

A small debug printing module that prints extra info like filenames,
function names, and line numbers. It can also recursively print objects
such as lists, tuples, and dicts.

More useful stuff may be added in the future.

Example Usage:
--------------

### Debug printing:

```python
from printdebug import debug
def myfunction():
    debug('Hello from myfunction.', basename=True)

myfunction()
```

####  Output:
```
   myfile.py:3 myfunction: Hello from myfunction.
```

### Formatting:

The default format for line information is `'{filename}:{lineno} {name}(): '`,
but can be set with the `fmt` arg:

```python
debug('Test', fmt='#{lineno} in function {name}, file: {filename}')
```

The format can be set once, and used every time with a `DebugPrinter` instance, or by overriding `printdebug.default_format`:

```python
from printdebug import DebugPrinter

dp = DebugPrinter(fmt='{filename}: {name}():#{lineno}')
dp.debug('Test')
```

### Print an object:

```python
from printdebug import printobject

o = {'key1': {'subkey1': 'value1', 'subkey2': 'value2'}}
printobject(o)
```

#### Output:
```
key1:
    subkey1:
        value1
    subkey2:
        value2
```

### Silencing debug prints:
`debug()` and `DebugPrinter()` can be silenced with `debug_enable(False)`:
```python
from printdebug import debug, debug_enable

debug('This will print.')

debug_enable(False)
debug('This will not.')

debug_enable()
debug('This will print now.')
```
