# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import trestapas
version = trestapas.__version__

setup(
    name='trestapas',
    version=version,
    author='Martín Gaitán',
    author_email='gaitan@gmail.com',
    packages=[
        'trestapas',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['trestapas/manage.py'],
)