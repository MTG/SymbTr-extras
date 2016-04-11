#!/usr/bin/env python

from setuptools import setup

setup(name='symbtrextras',
    version='0.3.dev',
    author='Sertan Senturk',
    author_email='contact AT sertansenturk DOT com',
    license='agpl 3.0',
    description='Basic tools to manipulate the SymbTr-scores',
    url='http://sertansenturk.com',
    packages=['symbtrextras'],
    include_package_data=True,
    install_requires=[
        "pandas",
    ],
)
