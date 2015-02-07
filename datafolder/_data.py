# -*- coding: utf-8 -*-

# datafolder - easy install and access to data files
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup data folder at the home directory of the effective user."""

import fnmatch
import os
import sys

from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH

from ._exceptions import DataFolderNotFoundError
from ._helpers import in_virtual


MODE666 = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH


class DataFolder(object):

    """Discover data folder and access to his files."""

    def __init__(self, foldername):
        """Set the basic class attributes."""
        if not foldername:
            raise DataFolderNotFoundError('Supply the name of the data folder')
        self.folderpath = self._find_location(foldername)
        # NOTE: sub-folders are NOT supported!
        self.filenames = os.listdir(self.folderpath)
        self.files = dict(((fn, os.path.join(self.folderpath, fn))
                           for fn in self.filenames))
        self.filepaths = list(self.files.values())

    @staticmethod
    def _find_location(foldername):
        """Find the location of the data folder."""
        raw_foldername = foldername
        foldername = foldername.strip('.')
        if in_virtual():
            data_dir = os.path.join(sys.prefix, foldername)
        else:
            if os.name == 'nt':
                data_dir = os.path.join(os.getenv('APPDATA'), foldername)
            else:
                data_dir = os.path.expanduser('~/.%s' % foldername)
        if not os.path.isdir(data_dir):
            raise DataFolderNotFoundError("Data folder '{}' wasn't found!"
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
