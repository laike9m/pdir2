"""
Tests category classification behavior
"""

import pdir
from pdir._internal_utils import category_match
from pdir.attr_category import AttrCategory as AC


class Base(object):
    base_class_variable = 1

    def __init__(self):
        self.base_instance_variable = 2

    def base_method(self):
        pass


class DerivedClass(Base):
    derived_class_variable = 1

    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        pass

    def __init__(self):
        self.derived_instance_variable = 2
        super(DerivedClass, self).__init__()

    def derived_method(self):
        pass


def test_no_arg():
    class C(object):
        pass

    class E(Exception):
        pass

    def f():
        pass

    p = 'foo'

    expected = {
        'C': AC.CLASS,
        'E': AC.EXCEPTION,
        'f': AC.FUNCTION,
        'p': AC.PROPERTY,
    }

    for pattr in pdir().pattrs:
        if pattr.name in expected:
            assert category_match(pattr.category, expected[pattr.name])
            expected.pop(pattr.name)

    # nothing left out
    assert len(expected) == 0
    # a joke: how about `assert not expected`


def test_class_instance():
    inst = DerivedClass()

    expected = {
        'base_class_variable': AC.CLASS_VARIABLE,
        'derived_class_variable': AC.CLASS_VARIABLE,
        'base_instance_variable': AC.INSTANCE_VARIABLE,
        'derived_instance_variable': AC.INSTANCE_VARIABLE,
        'static_method': AC.STATIC_METHOD,
        'class_method': AC.CLASS_METHOD,
    }

    for pattr in pdir(inst).pattrs:
        if pattr.name in expected:
            assert category_match(pattr.category, expected[pattr.name])
            expected.pop(pattr.name)

    # nothing left out
    assert len(expected) == 0
