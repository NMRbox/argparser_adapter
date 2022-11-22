#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    readme_long_description = fh.read()

setup(name = 'argparser_adapter',
    version = '1.4',
    url = 'https://nmrhub.org',
    maintainer = 'gweatherby',
    maintainer_email = 'gweatherby@uchc.edu',
    description = 'Add argparser argument based on object heuristics',
    long_description = readme_long_description,
    classifiers = ['License :: OSI Approved :: MIT License'],
    packages = find_packages() ,
    project_urls={
        'Funding' :'https://nmrhub.org'
    }
    )


