#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

setup(
    name='simurg',
    version='0.0.1',
    description='A Dataset for Training and Testing Abstractive Summarizers',
    url='http://dbs.cs.uni-duesseldorf.de',
    author='Pashutan Modaresi',
    author_email='modaresi@cs.uni-duesseldorf.de',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['scrapy']
)
