# -*- coding: utf-8 -*-

"""Make setup.py template and bootdf.py bootloader and service."""

import os

from ._resources import BOOT, TEMPLATE

TPL_FILE = 'setup_TPL.py'
BOOT_FILE = 'bootdf.py'


def mkboot():
    """Make bootloader file."""
    with open(BOOT_FILE, 'w') as f:
        f.write(BOOT)


def mktpl():
    """Make template."""
    with open(TPL_FILE, 'w') as f:
        f.write(TEMPLATE)
