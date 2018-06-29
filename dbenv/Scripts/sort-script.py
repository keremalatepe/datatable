#!c:\users\pc-358\desktop\flaskdb\dbenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sort==0.1.0','console_scripts','sort'
__requires__ = 'sort==0.1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sort==0.1.0', 'console_scripts', 'sort')()
    )
