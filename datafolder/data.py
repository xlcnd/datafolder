
"""Setup data folder at the home directory of the effective user."""

import os
import sys
import fnmatch
from stat import S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, S_IWOTH
from .helpers import in_virtual


MODE666 = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH


class DataFolder(object):

    def __init__(self, foldername):
        """Set the basic class attributes."""
        if in_virtual():
            data_dir = sys.prefix
        else:
            if os.name == 'nt':
                data_dir = os.path.join(os.getenv('APPDATA'), foldername)
            else:
                data_dir = os.path.expanduser('~/.%s' % foldername)
        self.folderpath = data_dir
        self.filenames = os.listdir(data_dir)
        self.files = dict(((fn, os.path.join(self.folderpath, fn)) for fn in self.filenames))
        self.filepaths = list(self.files.values())

    def writable(self, fn):
        """Verify if a file in the data folder is writable."""
        return os.access(self.files[fn], os.W_OK)
        
    def exists(self, fn):
        """Check if a file exists in the data folder."""
        return True if os.path.isfile(self.files[fn]) else False

    def splitext(self, fn):
        """Split the filename in name and extension."""
        return os.path.splitext(fn)

    def uxchmod(self, fn, mode=MODE666):
        """Change the mode of the file (default is 0666)."""
        return os.chmod(self.files[fn], mode)

    def select(pattern='*'):
        """List of data files that match a given pattern."""
        return fnmatch.filter(self.filenames, pattern)


        
    

