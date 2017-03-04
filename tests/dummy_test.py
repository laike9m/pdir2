import os
import sys
import pytest

import pdir


def test_pdir_module():
    print('test_pdir_module:')
    print(pdir(os))


def test_pdir_class():
    print('test_pdir_class:')
    print(pdir(list))


def test_pdir_object():
    print('test_pdir_object:')
    print(pdir([]))
