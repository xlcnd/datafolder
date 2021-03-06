# -*- coding: utf-8 -*-
# setup.py template made by the 'datafolder' package 
# for the datafolder project.


import sys
import pkg_resources

from setuptools import find_packages, setup

from datafolder.bootdf import Installer, DataFolderException

# write the name of the package (in this case 'mypkg'!)
MYPKG = 'datafolder'

# datafolder supports these python versions
SUPPORT = ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4')        # <-- ADAPT THIS

# list of data files in datafolder (just the names)
# [don't forget to include these files in MANIFEST.in!]
MYDATAFILES = ['test.conf', 'test.cvs', 'test.dat', 'test.db', 'test.yaml', 'çtest.pdf']


# (many people get confused with the next step...)


# tell setup were these files are in your package
# (I assume that they are together with the first __init__.py)
MYRESOURCES = [pkg_resources.resource_filename(MYPKG, datafile)
               for datafile in MYDATAFILES]


# now, create the installer
installer = Installer(sys.argv)

# use the installer to check supported python versions
installer.support(SUPPORT)

# create the data folder and tell setup to put the data files there
try:
    DATAPATH = installer.data_path(MYPKG)
except DataFolderException:
    # here you can handle any exception raised with the creation
    # of the data folder, e.g., abort installation
    print('Abort installation!')
    raise
data_files = [(DATAPATH, MYRESOURCES)]

# now, setup can do his thing...
setup(
    name=MYPKG,
    packages=find_packages(),
    data_files=data_files,
    ...                                                     # <-- ADAPT THIS
)

# but we are NOT READY, in some cases the data files
# don't have the appropriate permissions,
# let's fix that...
installer.pos_setup(MYDATAFILES)
