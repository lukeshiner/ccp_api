#!/usr/bin/env python
"""Setup for pywowcher package."""

from pathlib import Path

import setuptools

with open("README.rst", "r") as readme:
    long_description = readme.read()

version_file_path = Path(__file__).parent.joinpath("src", "ccp_api", "__version__.py")

about = {}
with open(str(version_file_path)) as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about["__release__"],
    description=about["__description__"],
    long_description=long_description,
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    keywords=["cloud commerce pro", "api", "e-commerce"],
    install_requires=["zeep", "pyaml"],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    python_requires=">=3.4.0",
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Other/Nonlisted Topic",
    ],
)
