"""Minimal setup file for Ring-Up project"""

from setuptools import setup, find_packages

setup(
        name='ringup_bsolis19',
        license='',

        author='Ben Solis',

        packages=find_packages(where='src'),
        package_dir={'': 'src'},
)
