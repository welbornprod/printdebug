PrintDebug
==========

A small debug printing module that prints extra info like filenames,
function names, and line numbers.

More useful stuff may be added in the future.

Example Usage:
--------------

    from printdebug import printdebug
    def myfunction():
        printdebug('Hello from myfunction.')

    myfunction()

    # Output: myfile.py line #3 in myfunction: Hello from myfunction.


