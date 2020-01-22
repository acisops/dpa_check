#!/usr/bin/env python
from setuptools import setup
from dpa_check import __version__

entry_points = {'console_scripts': 'dpa_check = dpa_check.dpa_check:main'}

url = 'https://github.com/acisops/dpa_check/tarball/{}'.format(__version__)

setup(name='dpa_check',
      packages=["dpa_check"],
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      description='ACIS Thermal Model for 1DPAMZT',
      author='John ZuHone',
      author_email='jzuhone@gmail.com',
      url='http://github.com/acisops/dpa_check',
      download_url=url,
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
      ],
      entry_points=entry_points,
      )
