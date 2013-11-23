#! /usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name = "vmflib",
    version = "0.1",
    packages = find_packages(),
    scripts = ['tools/buildbsp.py'],

    entry_points = {
        'console_scripts': [
            'buildbsp = buildbsp:main'
        ]
    },

    # metadata for upload to PyPI
    author = "Stephen Eisenhauer",
    author_email = "bhs2007@gmail.com",
    description = "A package for creating Valve Map Format (VMF) files for the Source engine",
    license = "BSD",
    keywords = "vmf valve map format source engine",
    url = "http://github.com/BHSPitMonkey/vmflib", 
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        ],
    long_description = """\
Tools for creating Valve Map Format (VMF) files
-----------------------------------------------

vmflib is a python module to help developers create maps for VMF-compatible 
video games procedurally using Python. The VMF format is best known for its 
use in the Source Engine and its many games.

Also included is a script (buildbsp) to help automate the process of compiling
and installing VMF maps into ready-to-use BSP files.

This package requires Python 3 or later.
"""
)
