#!c:\users\baic\downloads\apps\python37_x86\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'netease==1.0.3','console_scripts','netease-dl'
__requires__ = 'netease-dl==1.0.3'
from pkg_resources import load_entry_point

if __name__ == '__main__':
    myfunc = load_entry_point('netease-dl==1.0.3', 'console_scripts', 'netease-dl')
    myfunc('--help')
    myfunc(['song', '--id', '168158'])
