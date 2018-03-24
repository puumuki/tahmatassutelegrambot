# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="Tahmatassubot",
    version="1.0.0",
    description="Tahmatassu Telegram Bot",
    license="MIT",
    author="Teemu Puukko",
    packages=find_packages(),
    install_requires=['requests'],
    long_description=long_description,
    test_suite='runtest',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
    ]
)
