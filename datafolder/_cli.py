# -*- coding: utf-8 -*-

"""Make setup.py template and bootdf.py bootloader and service."""

import os
import sys
from shutil import copy2 as copyfile

from ._resources import BOOT, TPLDUMB, TPLSMART

PY2 = sys.version < '3'
TPL_FILE = 'setup_TPL.py'
BOOT_FILE = 'bootdf.py'
PYFILES = ('.py', '.pyc', '.pyw', '.po', '.pyo')
MANIFESTDEF = ('*.txt', '*.rst', '*.md')
WINDOWS = os.name == 'nt'
EOL = '\r\n' if WINDOWS and not PY2 else '\n'


def write2file(fp, text):
    """Helper to write to a file."""
    with open(fp, 'w') as f:
        f.write(text)


def backup_file(fp):
    """Append _ORIGINAL or _BACKUP to the file name."""
    if os.path.isfile(fp):
        name, ext = os.path.splitext(fp)
        newfp = name + '_ORIGINAL' + ext
        if os.path.isfile(newfp):
            newfp = name + '_BACKUP' + ext
        return copyfile(fp, newfp)
    return


def mkboot(projdir=None):
    """Make bootloader file."""
    prjboot = os.path.join(projdir, BOOT_FILE) if projdir else BOOT_FILE
    write2file(prjboot, BOOT)


def mktpl():
    """Make template."""
    write2file(TPL_FILE, TPLDUMB)


def mkmanifest(content, fp='MANIFEST.in'):
    """Make 'MANIFEST.in'."""
    if os.path.isfile(fp):
        with open(fp, 'r') as f:
            old_content = f.read()
        content = content + old_content
        content = EOL.join(sorted(set(content.strip(EOL).split(EOL))))
    write2file(fp, content)


def dirfiles(path):
    """Generator for files in directory 'path'."""
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            yield f


def datafiles(path):
    """Sorted list of datafiles, non python files, for directory 'path'."""
    return sorted([f for f in dirfiles(path) if os.path.splitext(f)[1].lower() not in PYFILES])


def exts(files):
    """Tuple of extensions of list of files."""
    return tuple(set([os.path.splitext(f)[1] for f in files if os.path.splitext(f)[1]]))


def noextfiles(files):
    """Tuple of files without extension in a list of files."""
    return tuple(set([f for f in files if not os.path.splitext(f)[1]]))


def usage():
    print('Usage: datafolder [PROJNAME|-m|-h|--help]')
    print('      -m    manual mode (generates bootdf.py and setup_TPL.py)')
    print('      -h    this message')
    sys.exit(1)


def parse(args):
    """Parses the sys.argv like args."""
    if len(args) < 2:
        return (args[0], None, True)
    if '-h' in args or '--help' in args:
        usage()
    if '-m' in args:
        return (args[0], None, True)
    return (args[0], args[1], False)


def main(args=None):
    if not args:
        args = sys.argv
    _, mypkg, manual = parse(args)
    if manual:
        mkboot()
        mktpl()
        print('Check the files %s and %s.' % (TPL_FILE, BOOT_FILE))
        sys.exit(0)
    if not os.path.isdir(mypkg):
        print('Project not found!')
        print('** Are you sure that you are at the root of the project?')
        sys.exit(1)
    print('Backup files...')
    backup_file('setup.py')
    backup_file('MANIFEST.in')
    df = datafiles(mypkg)
    dx = exts(df)
    if df:
        print('Making setup.py ...')
        dataf = "['" + "', '".join(df) + "']"
        content = TPLSMART.format(mypkg=mypkg, datafiles=dataf)
        write2file('setup.py', content)
        tpl = EOL + "include "
        content = "include " + tpl.join(MANIFESTDEF) + EOL
        tpl = EOL + "include {mypkg}/*"
        content += "include {mypkg}/*" + tpl.join(dx) + EOL
        noextf = noextfiles(df)
        if noextf:
            tpl = EOL + "include {mypkg}/"
            content += "include {mypkg}/" + tpl.join(noextf) + EOL
        content = content.format(mypkg=mypkg)
        print('Making MANIFEST.in ...')
        mkmanifest(content)
    print('Making bootdf.py inside %s ...' % mypkg)
    mkboot(mypkg)
