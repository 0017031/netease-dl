# -*- coding: utf-8 -*-

"""
@Author: ziwenxie
@Date:   2017-03-04 20:00:30
"""
import sys

from setuptools import setup, find_packages

install_requires = [
    'requests>=2.10.0',
    'pycryptodomex',
    'click>=5.1',
    'PrettyTable>=0.7.2',
    'mutagen', 'tqdm'
]

if sys.version_info[0] < 3:
    install_requires.append('win_unicode_console')

setup(
    name='myndl',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,

    entry_points='''
        [console_scripts]
        myndl=myndl.start:cli
    ''',

    license='MIT',
    # original_author='ziwenxie',
    # original_author_email='ziwenxiecat@gmail.com',
    author='baic',
    # url='https://github.com/0017031/myndl',
)
