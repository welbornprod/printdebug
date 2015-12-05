PrintDebug
==========

A small debug printing module that prints extra info like filenames,
function names, and line numbers. It can also recursively print objects
such as lists, tuples, and dicts.

More useful stuff may be added in the future.

Example Usage:
--------------

```python
    from printdebug import debug, printobject
    def myfunction():
        debug('Hello from myfunction.', basename=True)

    myfunction()

    # Output:
    #   myfile.py:3 myfunction: Hello from myfunction.

    o = {'key1': {'subkey1': 'value1', 'subkey2': 'value2'}}
    printobject(o)

    # Output:
    #    key1:
    #        subkey1:
    #            value1
    #        subkey2:
    #            value2
```


