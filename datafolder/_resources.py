# -*- coding: utf-8 -*-

"""Make setup.py template."""

import os
import sys

TPL_FILE = 'setup_TPL.py'

TEMPLATE = r"""
# setup.py template make by the 'datafolder' package


import sys
import pkg_resources
from setuptools import setup
from datafolder import Installer
#...

# write the name of the package (in this case 'mypkg'!)
MYPKG = 'mypkg'                                             #<-- ADAPT THIS

# mypkg supports these python versions?
SUPPORT = ((2, 6), (2, 7), (3, 1), (3, 2), (3, 3), (3, 4))  #<-- ADAPT THIS

# list of data files in mypkg (just the names)
MYDATAFILES = ['mypkg.conf', 'mypkg.db']                    #<-- ADAPT THIS


# (many people get confused with the next step...)


# tell setup were these files are in your package
# (I assume that are together with the first __init__.py)
MYRESOURCES = []
for datafile in MYDAFILES:
    MYRESOURCES.append(pkg_resources.resource_filename(MYPKG, datafile))


# now, create the installer
installer = Installer(sys.argv)

# use the installer to check supported python versions
installer.support(SUPPORT)

# create the data folder and tell setup to put the data files there
DATAPATH = installer.data_path(MYPKG)
data_files = [(DATAPATH, MYRESOURCES)]

# setup can now do his thing...
setup(
    name=MYPKG,
    data_files=data_files,
    install_requires=["datafolder>=0.0.4"],                 # <-- IMPORTANT
    ...                                                     # <-- ADAPT THIS
)

# but we are NOT READY, in some cases the data files
# don't have the appropriate permissions,
# let us fix that...
installer.pos_setup(MYDATAFILES)
"""

def mktpl():
    """Make template."""
    with open(TPL_FILE, 'w') as f:
        f.write(TEMPLATE)
