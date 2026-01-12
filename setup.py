#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for ParagliderLineTrim
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='ParagliderLineTrim',
    version='0.1',
    description='Python app dedicated to trimming of paraglider line length',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Loic',
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=[
        'PyQt5>=5.9.2',
        'matplotlib>=3.0.0',
        'numpy>=1.18.0',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'linetrim=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'resources': ['images/*'],
        'data': ['gliders/*', 'profiles/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
