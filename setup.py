#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='phototools',
      version='1.0',
      description='Tools for manipulating the Boyd photo collection',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      packages = find_packages(),
      entry_points = {'console_scripts': ['pt_sort = phototools.sort:run',
                                          'pt_index_html = phototools.index_html:run',
                                          'pt_thumb = phototools.preview:run_thumb',
                                          'pt_preview = phototools.preview:run_preview',
                                          ]}
     )
