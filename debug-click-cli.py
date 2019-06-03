#!c:\users\baic\downloads\apps\python37_x86\python.exe
# coding=utf-8
# EASY-INSTALL-ENTRY-SCRIPT: 'myndl==1.0.3','console_scripts','myndl'
# from myndl.download import NetEase

__requires__ = 'myndl==1.0.3'
from pkg_resources import load_entry_point

if __name__ == '__main__':
    myfunc = load_entry_point('myndl==1.0.3', 'console_scripts', 'myndl')
    # myfunc('--help')
    myfunc(['song', '--id', '168158'])
    # myfunc(['song', '--id', '168087'])

    # myfunc(['artist', '--id', '5770'])
    # myfunc(['artist', '--name', 'xuwei'])

    # myfunc(['album', '--name', u'在路上'])
    # myfunc(['album', '--id', u'16954'])

    # myfunc(['album', '--id', u'16946'])
    # myfunc(['-z', 'album', '--id', u'16946'])
    # myfunc(['playlist', '--id', u'2820918792'])
