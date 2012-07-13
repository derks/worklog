#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import worklog

setup(
    name='worklog',
    version=worklog.__version__,
    description='WorkLog',
    author='Jan Matejka',
    author_email='yac@blesmrt.net',
    url='https://github.com/yaccz/worklog',

    packages = find_packages(
        where = '.'
    ),

    install_requires = [
        "cement", # aliases will need probably like >1.9.12 which hasnt been released yet
        "setuptools",
        "sqlalchemy",
        "pyxdg",
        "pysqlite",
    ],

    entry_points = {
        'console_scripts': ['wl = worklog.core:main']},
)
