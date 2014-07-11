# -*- coding: utf-8 -*-

import sys


def in_virtual():
    return True if hasattr(sys, 'real_prefix') else False
