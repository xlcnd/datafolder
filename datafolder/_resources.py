# -*- coding: utf-8 -*-

"""Template strings for setup.py and bootdf.py."""


TPLSMART = r'''# -*- coding: utf-8 -*-
# setup.py template made by the 'datafolder' package
# for the {mypkg} project.

# If you need help about packaging, read
# https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html


import sys
import pkg_resources

from setuptools import find_packages, setup

from {mypkg}.bootdf import Installer, DataFolderException

# write the name of the package (in this case 'mypkg'!)
MYPKG = '{mypkg}'

# {mypkg} supports these python versions
SUPPORT = ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4')        # <-- ADAPT THIS

# list of data files in {mypkg} (just the names)
# [don't forget to include these files in MANIFEST.in!]
MYDATAFILES = {datafiles}


# (many people get confused with the next step...)


# tell setup were these files are in your package
# (I assume that they are together with the first __init__.py)
MYRESOURCES = [pkg_resources.resource_filename(MYPKG, datafile)
               for datafile in MYDATAFILES]


# now, create the installer
installer = Installer(sys.argv)

# use the installer to check supported python versions
installer.support(SUPPORT)

# checks if there are already data files and makes a backup
installer.backup(MYPKG, files=MYDATAFILES)

# create the data folder and tell setup to put the data files there
try:
    DATAPATH = installer.data_path(MYPKG)
except DataFolderException:
    # here you can handle any exception raised with the creation
    # of the data folder, e.g., abort installation
    raise Exception('Abort installation!')
data_files = [(DATAPATH, MYRESOURCES)]

# now, setup can do his thing...
setup(
    name=MYPKG,
    packages=find_packages(),
    data_files=data_files,
    author='',                 # <-- ADAPT THIS
    author_email='...@...',    # <-- ADAPT THIS
    url='',                    # <-- ADAPT THIS
    license='',                # <-- ADAPT THIS
    description='',            # <-- ADAPT THIS
    classifiers=[
        'Programming Language :: Python',
        ...  # <-- ADAPT THIS (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    ],
)

# but we are NOT READY, in some cases the data files
# don't have the appropriate permissions and 'pip'
# overwrites all data files that have been
# previously installed (even if they have been changed!).
# By default '.conf', '.cfg', '.ini' and '.yaml' files
# are protected, you can change this by passing
# parameter 'fns', e.g. fns=('*.db','data.csv'), to 'pos_setup'.
installer.pos_setup(MYDATAFILES)
'''


TPLDUMB = r'''# -*- coding: utf-8 -*-
# setup.py template made by the 'datafolder' package

# If you need help about packaging, read
# https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html


import sys
import pkg_resources

from setuptools import setup

from mypkg.bootdf import Installer, DataFolderException     # <-- ADAPT THIS

# write the name of the package (in this case 'mypkg'!)
MYPKG = 'mypkg'                                             # <-- ADAPT THIS

# mypkg supports these python versions
SUPPORT = ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4')        # <-- ADAPT THIS

# list of data files in mypkg (just the names)
# [don't forget to include these files in MANIFEST.in!]
MYDATAFILES = ['mypkg.conf', 'mypkg.db']                    # <-- ADAPT THIS


# (many people get confused with the next step...)


# tell setup were these files are in your package
# (I assume that they are together with the first __init__.py)
MYRESOURCES = [pkg_resources.resource_filename(MYPKG, datafile)
               for datafile in MYDATAFILES]

# now, create the installer
installer = Installer(sys.argv)

# use the installer to check supported python versions
installer.support(SUPPORT)

# checks if there are already data files and makes a backup
installer.backup(MYPKG, files=MYDATAFILES)

# create the data folder and tell setup to put the data files there
try:
    DATAPATH = installer.data_path(MYPKG)
except DataFolderException:
    # here you can handle any exception raised with the creation
    # of the data folder, e.g., abort installation
    raise Exception('Abort installation!')
data_files = [(DATAPATH, MYRESOURCES)]

# now, setup can do his thing...
setup(
    name=MYPKG,
    packages=[MYPKG,'other_packg1'],  # <-- ADAPT THIS
    data_files=data_files,
    author='',                 # <-- ADAPT THIS
    author_email='...@...',    # <-- ADAPT THIS
    url='',                    # <-- ADAPT THIS
    license='',                # <-- ADAPT THIS
    description='',            # <-- ADAPT THIS
    classifiers=[
        'Programming Language :: Python',
        ...  # <-- ADAPT THIS (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    ],
)

# but we are NOT READY, in some cases the data files
# don't have the appropriate permissions and 'pip'
# overwrites all data files that have been
# previously installed (even if they have been changed!).
# By default '.conf', '.cfg', '.ini' and '.yaml' files
# are protected, you can change this by passing
# parameter 'fns', e.g. fns=('*.db','data.csv'), to 'pos_setup'.
installer.pos_setup(MYDATAFILES)
'''


BOOT = r'''# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
# File generated by the 'datafolder' package

# datafolder - easy install and access to data files

# The MIT License (MIT)

# Copyright (c) 2015 Alexandre Lima Conde

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

###         PUT THIS FILE INSIDE YOUR PROJECT

__version__ = '0.3.6'

import fnmatch
import os
import sys

from shutil import copy2 as copyfile
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH

PROTECT_DEFAULTS = ('*.conf', '*.cfg', '*.ini', '*.yaml')


## ENV

MODE666 = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH

LINUX = sys.platform == 'linux2'
OSX = sys.platform == 'darwin'
POSIX = os.name == 'posix'
WINDOWS = sys.platform == 'win32'

VIRTUAL = True if hasattr(sys, 'real_prefix') else False


## HELPERS

def find_location(foldername):
    """Find the location of the data folder."""
    foldername = foldername.strip('.')
    if VIRTUAL:
        data_dir = os.path.join(sys.prefix, foldername)
    else:
        if WINDOWS:
            data_dir = os.path.join(os.getenv('APPDATA'), foldername)
        else:
            places = (
                '/etc/.%s' % foldername,
                '/usr/local/bin/.%s' % foldername,
                '/usr/local/.%s' % foldername,
                os.path.expanduser('~/.local/.%s' % foldername),
                os.path.expanduser('~/.%s' % foldername)
            )
            data_dir = None
            for place in reversed(places):
                if os.path.isdir(place):
                    data_dir = place
                    break
    return data_dir if data_dir and os.path.isdir(data_dir) else None

def data_files(foldername):
    """Tuple of datafiles with full path."""
    folderpath = find_location(foldername)
    if not folderpath:
        return ()
    filenames = os.listdir(folderpath)
    return (os.path.join(folderpath, fn) for fn in filenames)

def backup_file(fp):
    """Append _ORIGINAL or _BACKUP to the file name."""
    if os.path.isfile(fp):
        name, ext = os.path.splitext(fp)
        newfp = name + '_ORIGINAL' + ext
        if os.path.isfile(newfp):
            newfp = name + '_BACKUP' + ext
        return copyfile(fp, newfp)
    return

def protect(datapath, fns=None):
    """Recovers 'protected' datafiles."""
    if not fns:
        fns = PROTECT_DEFAULTS
    fnsindir = os.listdir(datapath)
    fnprot = []
    for fn in fns:
        if '*' in fn:
            filels = fnmatch.filter(fnsindir, fn)
            fnprot.extend(filels)
        else:
            if fn in fnsindir:
                fnprot.append(file)
    if not fnprot:
        return False
    changed = False
    for fn in fnprot:
        fbase, ext = os.path.splitext(fn)
        backf = fbase + '_BACKUP' + ext
        backfp = os.path.join(datapath, backf)
        if os.path.isfile(backfp):
            fnp = os.path.join(datapath, fn)
            copyfile(backfp, fnp)
            print('file %s restored' % fn)
            changed = True
            continue
        orif = fbase + '_ORIGINAL' + ext
        orifp = os.path.join(datapath, orif)
        if os.path.isfile(orifp):
            fnp = os.path.join(datapath, fn)
            copyfile(orifp, fnp)
            print('file %s restored' % fn)
            changed = True
    return changed


## MAIN CLASSES

class DataFolderException(Exception):
    """Base exception for 'datafolder' package.

    Should't NOT be raised directly, but can be used as a
    catch-all exception for the package.

    """
    pass

class DataFolderNotMadeError(DataFolderException):
    pass

class PythonNotSupportedError(DataFolderException):
    pass

class DataFolderNotFoundError(DataFolderException):
    pass


class Installer(object):

    """Installs the datafiles."""

    def __init__(self, sysargv):
        self.ARGVS = sysargv
        self.FIRSTRUN = 'egg_info' in self.ARGVS
        self.PIP = '-c' in self.ARGVS
        self.INSTALL = any((m in self.ARGVS for m in ('install', 'develop')))\
            or self.PIP
        self.WINDOWS = os.name == 'nt'
        self.POSIX = POSIX
        self.OSX = OSX
        self.LINUX = LINUX
        self.VIRTUAL = VIRTUAL
        self.SECONDRUN = self.INSTALL and not self.FIRSTRUN
        self.CONFDIR = ''
        self.DATAPATH = ''
        self.PYSUPPORT = ()

    @staticmethod
    def _uxchown(fp):
        if self.WINDOWS:
            return
        from pwd import getpwnam, getpwuid
        from grp import getgrnam, getgrgid
        uid = getpwnam(os.getenv("SUDO_USER",
                                 getpwuid(os.getuid()).pw_name)).pw_uid
        gid = getgrnam(os.getenv("SUDO_USER",
                                 getgrgid(os.getgid()).gr_name)).gr_gid
        os.chown(fp, uid, gid)

    def env(self):
        return {'FIRSTRUN': self.FIRSTRUN,
                'SECONDRUN': self.SECONDRUN,
                'INSTALL': self.INSTALL,
                'WINDOWS': self.WINDOWS,
                'OSX': self.OSX,
                'LINUX': self.LINUX,
                'POSIX': self.POSIX,
                'VIRTUAL': self.VIRTUAL,
                'PYSUPPORT': self.PYSUPPORT,
                'DATAPATH': self.DATAPATH}

    def data_path(self, datadir):
        if not self.SECONDRUN:
            return
        datadir = datadir.strip('.')
        self.CONFDIR = '.' + datadir if not self.WINDOWS else datadir
        if self.VIRTUAL:
            virtualpath = sys.prefix
            installpath = os.path.join(virtualpath, datadir)
        else:
            user = '~%s' % os.getenv("SUDO_USER", '')
            homepath = os.path.expanduser(user)\
                if not self.WINDOWS else os.getenv('APPDATA')
            installpath = os.path.join(homepath, self.CONFDIR)
        if not os.path.isdir(installpath) and self.INSTALL:
            try:
                print('making data folder %s' % installpath)
                os.mkdir(installpath)
                if not self.WINDOWS:
                    self._uxchown(installpath)
            except:
                msg = 'Abort: data folder NOT made with path %s!' % installpath
                raise DataFolderNotMadeError(msg)
        self.DATAPATH = installpath
        return self.DATAPATH

    def backup(self, datadir, files=None):
        """Backup data files.

        On FIRSTRUN pip deletes the original files
        (even if they have been customized)
        and deletes the directory (if empty).
        """
        if not self.FIRSTRUN:
            # Do nothing!
            return False
        if files:
            datafolder = find_location(datadir)
            if not datafolder:
                return False
            dfiles = (os.path.join(datafolder,fn) for fn in files)
        else:
            dfiles = data_files(datadir)
            if not dfiles:
                return False
        for fp in dfiles:
            backup_file(fp)
        return True

    def pos_setup(self, datafiles, fns=None):
        if not self.WINDOWS and self.SECONDRUN:
            for dat in datafiles:
                datp = os.path.join(self.DATAPATH, dat)
                if not os.path.isfile(datp):
                    print("Warning: file %s doesn't exist!" % datp)
                    continue
                try:
                    self._uxchown(datp)
                    print('changing mode of %s to 666' % dat)
                except:
                    print('Warning: permissions not set for file %s' % dat)
        if self.SECONDRUN:
            protect(self.DATAPATH, fns)

    def support(self, pys=None):
        if not self.FIRSTRUN:
            return True
        if not pys:
            return True
        self.PYSUPPORT = pys
        py = sys.version[:3]
        if py not in self.PYSUPPORT:
            raise PythonNotSupportedError('Python %s is not supported!' % py)
        return True


class DataFolder(object):

    """Discover data folder and access to his files."""

    def __init__(self, foldername=None):
        """Set the basic class attributes."""
        if not foldername:
            # try the name of the current folder (~ package)
            foldername = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
            if not foldername:
                raise DataFolderNotFoundError('Supply the name of the data folder')
        self.folderpath = find_location(foldername)
        if not self.folderpath:
            raise DataFolderNotFoundError('Supply the name of the data folder')
        # NOTE: sub-folders are NOT supported!
        self.filenames = os.listdir(self.folderpath)
        self.files = dict(((fn, os.path.join(self.folderpath, fn))
                           for fn in self.filenames))
        self.filepaths = list(self.files.values())

    def writable(self, fn):
        """Verify if a file in the data folder is writable."""
        return os.access(self.files[fn], os.W_OK)

    def exists(self, path):
        """Check if the path is a file or a directory in the data folder."""
        return os.path.exists(os.path.join(self.folderpath, path))

    def isfile(self, fn):
        """Check if a file exists in the data folder."""
        return os.path.isfile(self.files[fn])

    def splitbasename(self, fn):
        """Split the basename (of a file) in name and extension."""
        return os.path.splitext(fn)

    def uxchmod(self, fn, mode=MODE666):
        """Change the mode of the file (default is 0666)."""
        return os.chmod(self.files[fn], mode)

    def select(self, pattern='*'):
        """List of data files that match a given pattern."""
        return fnmatch.filter(self.filenames, pattern)
'''
