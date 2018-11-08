"""
Test attrs that previously caused bugs.
"""

import pdir
from pdir._internal_utils import category_match
from pdir.attr_category import AttrCategory


def test_dataframe():
    from pandas import DataFrame

    result = pdir(DataFrame)
    for attr in result.pattrs:
        if attr.name in ('columns', 'index'):
            assert category_match(attr.category, AttrCategory.PROPERTY)


def test_type():
    result = pdir(type)
    for attr in result.pattrs:
        if attr.name == '__abstractmethods__':
            assert category_match(attr.category, AttrCategory.ABSTRACT_CLASS)
            return


def test_list():
    result = pdir(list)
    for attr in result.pattrs:
        if attr.name == 'append':
            assert category_match(attr.category, AttrCategory.FUNCTION)
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
        r = RevealAccess(10, 'var ' r'')

        def __init__(self):
            self.d = D()

        @property
        def p(self):
            'this is p'
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
            assert category_match(pattr.category, AttrCategory.DESCRIPTOR)
            assert pattr.doc == ('class D with getter, setter, deleter, ' 'this is D')
        if pattr.name == 'r':
            assert category_match(pattr.category, AttrCategory.DESCRIPTOR)
            assert pattr.doc == (
                'class RevealAccess with getter, setter, ' 'deleter, this is R'
            )
        if pattr.name == 'p':
            assert category_match(pattr.category, AttrCategory.DESCRIPTOR)
            assert pattr.doc == ('@property with getter, setter, ' 'deleter, this is p')


def test_override_dir():

    # In the class attrs in `__dir__()` can not be found in `__dict__`
    class ClassWithUserDefinedDir(object):
        def __dir__(self):
            return ['foo']

    inst = ClassWithUserDefinedDir()
    pattrs = pdir(inst).pattrs
    assert ('foo' in pdir(inst)) == ('foo' in dir(inst))
    assert ('foo' in [pattr.name for pattr in pattrs]) == ('foo' in dir(inst))
