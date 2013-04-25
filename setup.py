#!/usr/bin/env python

from distutils.core import setup

setup(name = 'python-keynote',
      version = '0.5',
      description = 'Apple Keynote 09 Parser',
      license = 'MIT',
      author = 'Paul Hildebrandt',
      author_email = 'paul_hildebrandt@yahoo.com',
      packages = ['KeynoteAPI'],

      install_requires=["lxml"],

     )
