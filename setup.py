#!/usr/bin/env python

import animebot

from setuptools import setup, find_packages

setup(
    name='animebot',
    version=animebot.__version__,
    description='Animetardia Discord Bot',
    author='RHT',
    author_email='123',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['animebot = animebot:main']
        }
)
