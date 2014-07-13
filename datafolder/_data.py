# -*- coding: utf-8 -*-

"""Setup data folder at the home directory of the effective user."""

import os
import sys
import fnmatch
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH
from ._helpers import in_virtual
from ._exceptions import DataFolderNotFoundError as NFErr


MODE666 = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH


class DataFolder(object):

    """Discover and access to files in data folder."""

    def __init__(self, foldername=None):
        """Set the basic class attributes."""
        self.folderpath = self._find_location(foldername)
        self.filenames = os.listdir(self.folderpath)
        self.files = dict(((fn, os.path.join(self.folderpath, fn))
                           for fn in self.filenames))
        self.filepaths = list(self.files.values())

    @staticmethod
    def _find_location(foldername):
        """Find the location of the data folder."""
        if foldername is None and not in_virtual():
            raise NFErr('Please supply the name of the data folder or '
                        'then go to a virtual env.')
        raw_foldername = foldername
        foldername =  foldername.strip('. ')
        if in_virtual():
            data_dir = sys.prefix
        else:
            if os.name == 'nt':
                data_dir = os.path.join(os.getenv('APPDATA'), foldername)
            else:
                data_dir = os.path.expanduser('~/.%s' % foldername)
        if not os.path.isdir(data_dir):
            raise NFErr("Data folder '{}' wasn't found!"
                .format(raw_foldername))
        return data_dir

    def writable(self, fn):
        """Verify if a file in the data folder is writable."""
        return os.access(self.files[fn], os.W_OK)

    def exists(self, path):
        """Check if the path is a file or a directory in the data folder."""
        return os.path.exists(self.files[path])

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
