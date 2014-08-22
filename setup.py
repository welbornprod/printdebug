#!/usr/bin/env python
'''
    PrintDebug Setup
    ...Handles pip installation for the printdebug module.
    -Christopher Welborn 08-21-2014
'''
from __future__ import print_function
from distutils.core import setup

# Convert github markdown to Pypi rst.
defaultdesc = 'Small debug printing module.'
try:
    import pypandoc
except ImportError:
    print('Pypandoc not installed, falling back to default description.')
    longdesc = defaultdesc
else:
    try:
        longdesc = pypandoc.convert('README.md', 'rst')
    except EnvironmentError:
        # Fallback to manually converted README.txt (may be behind on updates)
        try:
            with open('README.txt') as f:
                longdesc = f.read()
        except EnvironmentError:
            # Something is horribly wrong.
            print('Error reading README.md and fallback README.txt!')
            longdesc = defaultdesc

setup(
    name='PrintDebug',
    version='0.0.4',
    author='Christopher Welborn',
    author_email='cj@welbornprod.com',
    packages=['printdebug'],
    url='http://pypi.python.org/pypi/PrintDebug/',
    license='LICENSE.txt',
    description=open('DESC.txt').read(),
    long_description=longdesc,
    keywords='python module library 2 3 print debug ',
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
