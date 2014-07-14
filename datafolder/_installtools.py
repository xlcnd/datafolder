# -*- coding: utf-8 -*-

"""Setup data folder at the home directory of the effective user."""

import os
import sys

from ._exceptions import PythonNotSupportedError as PNSErr
from ._exceptions import DataFolderNotMadeError as DNMErr
from ._helpers import in_virtual


class Installer(object):

    """Setup data folder with the right permissions."""

    def __init__(self, sysargv):
        """Set env variables."""
        self.ARGVS = sysargv
        self.FIRSTRUN = 'egg_info' in self.ARGVS
        self.PIP = '-c' in self.ARGVS
        self.INSTALL = any((m in self.ARGVS for m in ('install', 'develop')))\
            or self.PIP
        self.WINDOWS = os.name == 'nt'
        self.VIRTUAL = in_virtual()
        self.SECONDRUN = self.INSTALL and not self.FIRSTRUN
        self.CONFDIR = ''
        self.DATAPATH = ''
        self.PYSUPPORT = ()

    @staticmethod
    def _uxchown(fp):
        from pwd import getpwnam, getpwuid
        from grp import getgrnam, getgrgid
        uid = getpwnam(os.getenv("SUDO_USER",
                                 getpwuid(os.getuid()).pw_name)).pw_uid
        gid = getgrnam(os.getenv("SUDO_USER",
                                 getgrgid(os.getgid()).gr_name)).gr_gid
        os.chown(fp, uid, gid)

    def env(self):
        """Return a dict with the status of several env variables."""
        return {'FIRSTRUN': self.FIRSTRUN,
                'SECONDRUN': self.SECONDRUN,
                'INSTALL': self.INSTALL,
                'WINDOWS': self.WINDOWS,
                'VIRTUAL': self.VIRTUAL,
                'PYSUPPORT': self.PYSUPPORT,
                'DATAPATH': self.DATAPATH}

    def data_path(self, datadir):
        """Make the data folder with the rigth permissions."""
        datadir = datadir.strip('. ')
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
                self._uxchown(installpath)
            except:
                raise DNMErr('Abort: data folder NOT made!')
        self.DATAPATH = installpath
        return self.DATAPATH

    def pos_setup(self, datafiles):
        """Change the data files permissions for UNIX files."""
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

    def support(self, pys):
        """Check if the python being used for the install is supported."""
        self.PYSUPPORT = pys
        py = tuple(int(x) for x in sys.version[:3].split('.'))
        if py not in self.PYSUPPORT:
            raise PNSErr('Python %s.%s is not supported!' % py)
        return True
