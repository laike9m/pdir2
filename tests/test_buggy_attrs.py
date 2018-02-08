"""
Test attrs that previously caused bugs.
"""

import pdir

from pdir.constants import AttrCategory


def test_dataframe():
    from pandas import DataFrame
    result = pdir(DataFrame)
    for attr in result.pattrs:
        if attr.name in ('columns', 'index'):
            assert attr.category == AttrCategory.DEFAULT_CATEGORY


def test_type():
    result = pdir(type)
    for attr in result.pattrs:
        if attr.name == '__abstractmethods__':
            assert attr.category == AttrCategory.ABSTRACT_CLASS
            return


def test_list():
    result = pdir(list)
    for attr in result.pattrs:
        if attr.name == 'append':
            assert attr.category == AttrCategory.FUNCTION
            return


class D(object):
    """this is D"""

    def __init__(self):
        pass

    def __get__(self, instance, type=None):
        pass

    def __set__(self, instance, value):
        pass

    def __delete__(self, obj):
        pass


class RevealAccess(object):
    """this is R"""

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

    def __delete__(self, obj):
        pass


def test_descriptor():
    class T(object):
        r = RevealAccess(10, 'var "r"')

        def __init__(self):
            self.d = D()

        @property
        def p(self):
            "this is p"
            return 1

        @p.setter
        def p(self):
            pass

        @p.deleter
        def p(self):
            pass

    t = T()
    pattrs = pdir(t).pattrs
    for pattr in pattrs:
        if pattr.name == 'd':
            assert pattr.category == AttrCategory.DESCRIPTOR
            assert pattr.doc == ('class D with getter, setter, deleter, '
                                 'this is D')
        if pattr.name == 'r':
            assert pattr.category == AttrCategory.DESCRIPTOR
            assert pattr.doc == ('class RevealAccess with getter, setter, '
                                 'deleter, this is R')
        if pattr.name == 'p':
            assert pattr.category == AttrCategory.DESCRIPTOR
            assert pattr.doc == ('@property with getter, setter, '
                                 'deleter, this is p')
