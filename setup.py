#!/user/bin/env python3 

from setuptools import setup

setup(
    name = 'gitdown',
    version = '1.0',
    package = ['gitdown'],
    entry_points = {
        'console_scripts' : ['gitdown = gitdown.cli:main']
    }
)