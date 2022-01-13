"""
Tests attribute filter's behaviors.
"""

import collections
import sys

import pdir


# https://github.com/python/cpython/blob/da2bf9f66d0c95b988c5d87646d168f65499b316/Lib/unittest/case.py#L1164-L1195
def items_equal(first, second):
    """A simplified version of the unittest.assertEqual method."""
    first_seq, second_seq = list(first), list(second)
    first = collections.Counter(first_seq)
    second = collections.Counter(second_seq)
    return first == second


class Base:
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
    assert items_equal(
        [p.name for p in pdir(inst).properties.pattrs],
        [
            'base_class_variable',
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
            '__class__',
            '__dict__',
            '__doc__',
            '__module__',
            '__weakref__',
        ],
    )


def test_methods():
    if sys.version[0] == '2':
        assert items_equal(
            [p.name for p in pdir(inst).methods.pattrs],
            [
                '__subclasshook__',
                '__delattr__',
                '__getattribute__',
                '__setattr__',
                'base_method',
                'derived_method',
                '__format__',
                '__hash__',
                '__init__',
                '__new__',
                '__repr__',
                '__sizeof__',
                '__str__',
                '__reduce__',
                '__reduce_ex__',
            ],
        )
    else:
        assert items_equal(
            [p.name for p in pdir(inst).methods.pattrs],
            [
                '__subclasshook__',
                '__delattr__',
                '__dir__',
                '__getattribute__',
                '__setattr__',
                '__init_subclass__',
                'base_method',
                'derived_method',
                '__format__',
                '__hash__',
                '__init__',
                '__new__',
                '__repr__',
                '__sizeof__',
                '__str__',
                '__reduce__',
                '__reduce_ex__',
                '__eq__',
                '__ge__',
                '__gt__',
                '__le__',
                '__lt__',
                '__ne__',
            ],
        )


def test_public():
    assert items_equal(
        [p.name for p in pdir(inst).public.pattrs],
        [
            'base_method',
            'derived_method',
            'base_class_variable',
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
        ],
    )


def test_own():
    assert items_equal(
        [p.name for p in pdir(inst).own.pattrs],
        [
            'derived_method',
            '__init__',
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
            '__doc__',
            '__module__',
        ],
    )


def test_chained_filters():
    assert items_equal(
        [p.name for p in pdir(inst).public.own.properties.pattrs],
        [
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
        ],
    )


def test_order_of_chained_filters():
    assert items_equal(
        [p.name for p in pdir(inst).own.properties.public.pattrs],
        [
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
        ],
    )
    assert items_equal(
        [p.name for p in pdir(inst).properties.public.own.pattrs],
        [
            'base_instance_variable',
            'derived_class_variable',
            'derived_instance_variable',
        ],
    )


def test_filters_with_search():
    def test_chained_filters():
        assert items_equal(
            [
                p.name
                for p in pdir(inst).public.own.properties.search('derived_in').pattrs
            ],
            ['derived_instance_variable'],
        )
