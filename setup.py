#!/usr/bin/env python

from distutils.core import setup

from keynote_api import __version__

setup(name = 'python-keynote',
      version = __version__,
      description = 'Apple Keynote 09 Parser',
      license = 'MIT',
      author = 'Paul Hildebrandt',
      author_email = 'paul_hildebrandt@yahoo.com',
      packages = ['keynote_api'],

      install_requires=["lxml"],

     )
