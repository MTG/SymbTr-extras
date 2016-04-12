#!/usr/bin/env python
import subprocess
try:
    from setuptools import setup
    from setuptools import find_packages
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from setuptools import find_packages  # no replacement in distutils
    from distutils.command.install import install as _install


class CustomInstall(_install):
    def run(self):
        # install package
        _install.run(self)

        # install requirements
        subprocess.call(["pip install -Ur requirements"], shell=True)


setup(name='symbtrextras',
      version='0.3.0',
      author='Sertan Senturk',
      author_email='contact AT sertansenturk DOT com',
      license='agpl 3.0',
      description='Basic tools to manipulate the SymbTr-scores',
      url='http://sertansenturk.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          "pandas==0.18.0",
      ],
      )
