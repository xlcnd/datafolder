# -*- coding: utf-8 -*-

# datafolder - easy install of data files
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

__all__ = ('DataFolder',
           'mktpl',
           'mkboot',
           'DataFolderException',
           'DataFolderNotFoundError')

__version__ = '0.0.9'                        # <-- literal IDs
__support__ = ((2, 6), (2, 7), (3, 1), (3, 2), (3, 3), (3, 4))

from ._data import DataFolder
from ._exceptions import (DataFolderException, DataFolderNotFoundError)
from ._resources import mktpl, mkboot
