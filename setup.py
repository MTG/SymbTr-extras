#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages


setup(name='symbtrextras',
      version='0.3.2',
      author='Sertan Senturk',
      author_email='contact AT sertansenturk DOT com',
      license='agpl 3.0',
      description='Basic tools to manipulate the SymbTr-scores',
      url='http://sertansenturk.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          "pandas==0.18.0",
          "future"
      ],
      )
