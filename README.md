PrintDebug
==========

A small debug printing module that prints extra info like filenames,
function names, and line numbers. It can also recursively print objects
such as lists, tuples, and dicts.

More useful stuff may be added in the future.

Example Usage:
--------------

    from printdebug import printdebug, printobject
    def myfunction():
        printdebug('Hello from myfunction.')

    myfunction()

    # Output:
    #   myfile.py line #3 in myfunction: Hello from myfunction.

    o = {'key1': {'subkey1': 'value1', 'subkey2': 'value2'}}
    printobject(o)

    # Output:
    #    key1:
    #        subkey1:
    #            value1
    #        subkey2:
    #            value2



