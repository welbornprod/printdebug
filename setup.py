#!/usr/bin/env python
'''
    PrintDebug Setup
    ...Handles pip installation for the printdebug module.
    -Christopher Welborn 08-21-2014
'''

from distutils.core import setup

setup(
    name='PrintDebug',
    version='0.0.2',
    author='Christopher Welborn',
    author_email='cj@welbornprod.com',
    packages=['printdebug'],
    url='http://pypi.python.org/pypi/PrintDebug/',
    license='LICENSE.txt',
    description=open('DESC.txt').read(),
    long_description=open('README.txt').read(),
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
