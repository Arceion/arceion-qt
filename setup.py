#!/usr/bin/env python
"""
Setup script for Arceion-Qt package
"""

from setuptools import find_packages, setup

setup(
    name="arceion-qt",
    version="0.1.0",
    description="Arceion Qt - A collection of Qt components",
    long_description=open("README.md", encoding="utf-8").read(),  # noqa: SIM115
    long_description_content_type="text/markdown",
    author="Arceion",
    author_email="arceionllc@gmail.com",
    url="https://github.com/Arceion/arceion-qt",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "PyQt6",
        "cryptography",
        "requests",
        "pytz",
        "icecream",
        "fontTools",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
