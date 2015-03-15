#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

import os
import sys

py_version = sys.version_info
version = ".".join([str(i) for i in __import__('xlsx').VERSION])

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Natural Language :: English',
    'Topic :: Utilities'
]

install_requires = [
    'six',
    'openpyxl==1.8.2',
    'XlsxWriter',
    'PyTMX',
    'lxml'
]


if isinstance(py_version, tuple):
    if py_version < (2, 7):
        install_requires.append('importlib')


setup(
    name='xlsx',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version=version,
    author_email='tarvitz@blacklibrary.ru',
    download_url='https://github.com/tarvitz/xlsx-dr/archive/master.zip',
    description='xlsx dirty reader',
    long_description=open(readme).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    packages=find_packages(exclude=['docs', 'requirements'],),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False)
