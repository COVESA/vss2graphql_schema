#!/usr/bin/env python3

# Copyright (C) 2021, Bayerische Motoren Werke Aktiengesellschaft (BMW AG),
#   Author: Alexander Domin (Alexander.Domin@bmw.de)
# Copyright (C) 2021, ProFUSION Sistemas e Soluções LTDA,
#   Author: Leonardo Ramos (leo.ramos@profusion.mobi)
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was
# not distributed with this file, You can obtain one at
# http://mozilla.org/MPL/2.0/.

# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

name = 'vss2graphql_schema'
version = 1
release = 0

setup(
    name=name,
    version=f'{version}.{release}',
    description='Parse VSS data structure to generate GraphQL artifacts',
    url='https://github.com/COVESA/vss2graphql_schema.git',  # noqa:E501
    python_requires='>=3.8',
    install_requires=[
        'jinja2',
        'pyyaml-include',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'vss2graphql_schema=vss2graphql_schema.vss2graphql_schema:main',
        ],
    },
    keywords='graphql_generators yaml vss vspec',
    classifiers=[
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    package_data={'vss2graphql_schema.graphql_generators': [
        'templates/*.jinja'
    ]},
)
