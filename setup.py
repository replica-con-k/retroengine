#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-

from setuptools import setup
import distutils_pytest

setup(name='retroengine',
      version='0.1',
      description='Library for make retro games easily',
      author='Int-0',
      author_email='tobias.deb@gmail.com',
      license='GPL v3.0',
      packages=['retro'],
      package_dir={'retro': 'retro'},
      zip_safe=False,
      setup_requires=['pytest-runner'],
      test_require=['pytest'])
