#!/usr/bin/python
# see https://pypi.org/project/python-rpm-spec-dependency-analyzer/

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rpm-spec-dependency-analyzer',
    packages=['rpm_spec_dependency_analyzer'],
    python_requires='>=3',
    version='0.5',
    description='Module for analyzing RPM spec dependencies.',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    author='Francesco Montorsi',
    author_email='francesco.montorsi@gmail.com',
    url='https://github.com/f18m/rpm-spec-dependency-analyzer',
    download_url='https://github.com/f18m/rpm-spec-dependency-analyzer/archive/1.0.tar.gz',
    keywords=['RPM', 'spec', 'graphviz', 'dependencies', 'dependency-analysis'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'rpm_spec_dependency_analyzer = rpm_spec_dependency_analyzer.rpm_spec_dependency_analyzer:main',
        ]
    }
)
