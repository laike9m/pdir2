"""
Tests attribute filter's behaviors.
"""

import sys

import pdir


class Base(object):
    base_class_variable = 1

    def __init__(self):
        self.base_instance_variable = 2

    def base_method(self):
        pass


class DerivedClass(Base):
    derived_class_variable = 1

    def __init__(self):
        self.derived_instance_variable = 2
        super(DerivedClass, self).__init__()

    def derived_method(self):
        pass


inst = DerivedClass()


def test_properties():
    assert [
        'base_class_variable', 'base_instance_variable',
        'derived_class_variable', 'derived_instance_variable', '__class__',
        '__dict__', '__doc__', '__module__', '__weakref__'
    ] == [p.name for p in pdir(inst).properties.pattrs]


def test_methods():
    if sys.version[0] == '2':
        assert [
            '__subclasshook__', '__delattr__', '__getattribute__',
            '__setattr__', 'base_method', 'derived_method', '__format__',
            '__hash__', '__init__', '__new__', '__repr__', '__sizeof__',
            '__str__', '__reduce__', '__reduce_ex__'
        ] == [p.name for p in pdir(inst).methods.pattrs]
    else:
        assert [
            '__subclasshook__', '__delattr__', '__dir__', '__getattribute__',
            '__setattr__', '__init_subclass__', 'base_method',
            'derived_method', '__format__', '__hash__', '__init__', '__new__',
            '__repr__', '__sizeof__', '__str__', '__reduce__', '__reduce_ex__',
            '__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__ne__'
        ] == [p.name for p in pdir(inst).methods.pattrs]


def test_public():
    assert [
        'base_method', 'derived_method', 'base_class_variable',
        'base_instance_variable', 'derived_class_variable',
        'derived_instance_variable'
    ] == [p.name for p in pdir(inst).public.pattrs]


def test_own():
    assert [
        'derived_method', '__init__', 'base_instance_variable',
        'derived_class_variable', 'derived_instance_variable', '__doc__',
        '__module__'
    ] == [p.name for p in pdir(inst).own.pattrs]


def test_public_own_properties():
    assert [
        'base_instance_variable',
        'derived_class_variable',
        'derived_instance_variable',
    ] == [p.name for p in pdir(inst).public.own.properties.pattrs]
