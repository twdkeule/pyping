#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
	return io.open(
		join(dirname(__file__), *names),
		encoding=kwargs.get('encoding', 'utf8')
	).read()


setup(
	name='pyping',
	version='0.0.6',
	license=open("LICENSE").read(),
	description='A python wrapper around the Linux ping command',
	long_description=read('README.rst'),
	author="Thomas De Keulenaer",
	author_email="thomas.dekeulenaer@gmail.com",
	url='https://github.com/twdkeule/pyping',
	packages=find_packages('src'),
	package_dir={'': 'src'},
	py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
		'Operating System :: Unix',
		'Operating System :: POSIX',
		"Intended Audience :: Education",
		"Intended Audience :: Developers",
		"Topic :: Education",
		'Topic :: Utilities',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6'
	],
	keywords=[
		"ping", "icmp", "latency"
	],
	install_requires=[
	],
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
	extras_require={
		# eg:
		#   'rst': ['docutils>=0.11'],
		#   ':python_version=="2.6"': ['argparse'],
	},
	entry_points={
		'console_scripts': [
			'nameless = nameless.cli:main',
		]
	},
)
