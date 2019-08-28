#!/usr/bin/python3
# Setup script to install this package.
# M.Blakeney, Mar 2018.

import re, stat
from pathlib import Path
from setuptools import setup

here = Path(__file__).resolve().parent
name = re.sub(r'-.*', '', here.stem)
readme = here.joinpath('README.md').read_text()
executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH

setup(
    name=name,
    version='1.8',
    description='Python module/program to control Watts Clever switch',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/bulletmark/{}'.format(name),
    author='Mark Blakeney',
    author_email='mark@irsaere.net',
    keywords='RPi',
    license='GPLv3',
    py_modules=[name],
    python_requires='>=3.4',
    install_requires=['RPi.GPIO'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        ('share/doc/{}'.format(name), ['README.md']),
    ],
    scripts=[f.name for f in here.iterdir()
        if f.is_file() and f.stat().st_mode & executable],
)
