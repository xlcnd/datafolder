# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import os

from nose.tools import assert_equals, assert_raises

from .bootdf import Installer, DataFolder


PACKGNAME = 'deleteme'
FILE1 = 'test.conf'
FILE2 = 'test.db'

installer = Installer(['python', 'setup.py', '-c'])
DATAPATH = installer.data_path(PACKGNAME)

FILES = [os.path.join(DATAPATH, FILE1), os.path.join(DATAPATH, FILE2)]


def create_files(files):
    os.chdir(os.path.dirname(files[0]))
    for fn in files:
        f = open(fn, 'w')
        f.write('')
        f.close()

def delete_files(files):
    os.chdir(os.path.dirname(files[0]))
    for fn in files:
        os.remove(fn)

def setup_module():
    create_files(FILES)


def teardown_module():
    delete_files(FILES)
    os.rmdir(DATAPATH)


inst_run1 = Installer(['python', 'setup.py', 'egg_info'])
inst_run2 = Installer(['python', 'setup.py', '-c'])



def test_env():
    assert inst_run1.env()['FIRSTRUN'] == True
    assert inst_run2.env()['SECONDRUN'] == True


def test_data_folder():
    assert_raises(Exception, DataFolder, 'xxx')
    dt = DataFolder(PACKGNAME)
    assert_equals(dt.select('*.db')[0], FILE2)



