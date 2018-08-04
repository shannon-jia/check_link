#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'aiohttp>=3.1.2',
                'asynqp>=0.5.1',
                'pymongo',
                'motor>=1.2']

setup_requirements = []

test_requirements = []

setup(
    author="Shannon-Li",
    author_email='lishengchen@mingvale.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Check Link",
    entry_points={
        'console_scripts': [
            'check-link=check_link.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='check_link',
    name='check_link',
    packages=find_packages(include=['check_link']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shannon-jia/check_link',
    version='1.0',
    zip_safe=False,
)
