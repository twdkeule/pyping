#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup

setup(
	name='pyping',
	version='0.0.1',
	description='A python wrapper around the Linux ping command',
	long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
	license=open("LICENSE").read(),
	author="Thomas De Keulenaer",
	author_email="thomas.dekeulenaer@",
	url='https://github.com/twdkeule/pyping',
	keywords=["ping", "icmp", "latency"],
	packages = ['pyping'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Programming Language :: Python :: 3.6"]
)
