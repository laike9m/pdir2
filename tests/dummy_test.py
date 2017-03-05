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


def test_dir_without_argument():
    a = 1
    b = 2

    def whatever():
        pass

    print('test dir()')
    print(dir())
    print(pdir())
