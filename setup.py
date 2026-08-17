#!/usr/bin/env python3

# Copyright (C) 2021 NTA, Inc.

from setuptools import setup, find_packages

setup(
    name="wumps",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "lark==1.3.1",
    ],
    entry_points={
        "console_scripts": [
            "wumps = wumps.scripts.process_wumps:main",
        ],
    },
)
