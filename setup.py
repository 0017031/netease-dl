# -*- coding: utf-8 -*-

"""
@Author: ziwenxie
@Date:   2017-03-04 20:00:30
"""
from setuptools import setup, find_packages

setup(
    name='netease-dl',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.10.0',
        'pycryptodomex',
        'click>=5.1',
        'PrettyTable>=0.7.2',
    ],

    entry_points='''
        [console_scripts]
        netease-dl=netease.start:cli
    ''',

    license='MIT',
    # original_author='ziwenxie',
    # original_author_email='ziwenxiecat@gmail.com',
    author='baic',
    url='https://github.com/0017031/netease-dl',
)
