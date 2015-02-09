# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import os

from nose.tools import assert_equals, assert_raises

from .._cli import dirfiles, datafiles, main



def test_main():
    cwdir = os.path.dirname(os.path.abspath(__file__)) 
    os.chdir(cwdir)
    main(['datafolder', 'prjname'])
    files = [f for f in dirfiles('prjname')]
    assert 'bootdf.py' in files
