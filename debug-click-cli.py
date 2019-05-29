#!c:\users\baic\downloads\apps\python37_x86\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'myndl==1.0.3','console_scripts','myndl'
__requires__ = 'myndl==1.0.3'
from pkg_resources import load_entry_point

if __name__ == '__main__':
    myfunc = load_entry_point('myndl==1.0.3', 'console_scripts', 'myndl')
    # myfunc('--help')
    myfunc(['song', '--id', '168158'])
    # myfunc(['artist', '--id', '5770'])
    # myfunc(['artist', '--name', 'xuwei'])
