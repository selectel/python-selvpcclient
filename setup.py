#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    setup_requires=['pbr>=5.4.5'],
    packages=find_packages(exclude=['tests']),
    pbr=True
)
