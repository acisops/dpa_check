#!/usr/bin/env python
from setuptools import setup

try:
    from testr.setup_helper import cmdclass
except ImportError:
    cmdclass = {}

entry_points = {'console_scripts': 'dpa_check = dpa_check.dpa_check:main'}

setup(name='dpa_check',
      packages=["dpa_check"],
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      description='ACIS Thermal Model for 1DPAMZT',
      author='John ZuHone',
      author_email='jzuhone@gmail.com',
      url='http://github.com/acisops/dpa_check',
      include_package_data=True,
      entry_points=entry_points,
      zip_safe=False,
      tests_require=["pytest"],
      cmdclass=cmdclass,
      )
