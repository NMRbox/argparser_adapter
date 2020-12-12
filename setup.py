#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    readme_long_description = fh.read()

setup(name = 'argparse_adapter',
    version = '1.0',
    url = 'http://www.nmrbox.org',
    maintainer = 'gweatherby',
    maintainer_email = 'gweatherby@uchc.edu',
    description = 'Add argparser argument based on object heuristics',
    long_description = readme_long_description,
    classifiers = ['License :: NMRbox license'],
    packages = find_packages() 
    )


