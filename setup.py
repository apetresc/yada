#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from distutils.command.upload import upload as UploadOrig

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = 'yada'
DESCRIPTION = ('Yet another dotfile aggregator')
URL = 'https://github.com/apetresc/yada'
EMAIL = 'adrian@apetre.sc'
AUTHOR = 'Adrian Petrescu'
REQUIRES_PYTHON = '>=2.7.15, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*'

REQUIRED = [
    'future>=0.16.0',
    'six>=1.10.0',
    'Click>=7.0,<8.0',
    'pathlib2==2.3.3;python_version<"3.4"',
    'pyyaml>=3.12,<6.0',
]

SETUP_REQUIRED = [
    'setuptools_scm'
]

EXTRAS = {
    'tests': [
        'pyfakefs',
        'pytest',
        'pytest-cov',
        'coverage',
    ],
    'linter': [
        'flake8',
        'flake8-broken-line;python_version>"3.5"',
        'flake8-builtins',
        'flake8-bugbear;python_version>"3.5"',
        'flake8-comprehensions;python_version>"3.5"',
        'flake8-eradicate;python_version>"3.5"',
        'flake8-pep3101',
        'flake8-print',
        'flake8-quotes',
    ]
}

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    use_scm_version=True,
    packages=find_packages(where='./src'),
    package_dir={'': 'src'},
    install_requires=REQUIRED,
    setup_requires=SETUP_REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data={'yada.data': ['config.yaml']},
    entry_points={
        'console_scripts': [
            'yada=yada.cli.main:cli'
        ]
    }
)
