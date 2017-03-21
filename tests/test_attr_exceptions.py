"""
Test attrs defined in ATTR_EXCEPTION_MAP.
"""

import pdir


def test_dataframe():
    from pandas import DataFrame
    result = pdir(DataFrame)
    for attr in result.attrs:
        if attr.name in ('columns', 'index'):
            assert attr.category == 'other'


def test_type():
    result = pdir(type)
    for attr in result.attrs:
        if attr.name == '__abstractmethods__':
            assert attr.category == 'abstract class'
            return


def test_none():
    dir_attrs = dir(None)
    pdir_attrs = list(dir(None))
    assert dir_attrs == pdir_attrs
