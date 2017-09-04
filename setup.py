#!/usr/bin/env python3


from setuptools import setup, find_packages


setup(
    name='pysteamcli',
    version='0.1',
    packages=find_packages(),
    author='Lior Stern',
    description='Use Steam from the comfort of your terminal',
    license='MIT',
    entry_points={
        'console_scripts': ['pysteamcli=pysteamcli.__main__:main']
    }
)
