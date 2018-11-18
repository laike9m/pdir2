"""
Test classes with __slots__
"""

from typing import List

import pdir
from pdir.attr_category import AttrCategory, category_match


BASE = 'base'
DERIVE = 'derive'


class BaseNoSlot:
    pass


class BaseEmptySlot:
    __slots__: List[str] = []


class BaseSlot:
    __slots__: List[str] = [BASE]


class DeriveNoSlotBaseEmpty(BaseEmptySlot):
    pass


class DeriveNoSlotBaseSlot(BaseSlot):
    pass


class DeriveEmptySlotBaseNo(BaseNoSlot):
    __slots__: List[str] = []


class DeriveEmptySlotBaseEmpty(BaseEmptySlot):
    __slots__: List[str] = []


class DeriveEmptySlotBaseSlot(BaseSlot):
    __slots__: List[str] = []


class DeriveSlotBaseNo(BaseNoSlot):
    __slots__ = [DERIVE]


class DeriveSlotBaseEmpty(BaseEmptySlot):
    __slots__ = [DERIVE]


class DeriveSlotBaseSlot(BaseSlot):
    __slots__ = [DERIVE]


def test_not_set():
    expected_res = [  # class type    empty slot attr num
        (DeriveNoSlotBaseEmpty, 0),
        (DeriveNoSlotBaseSlot, 1),
        (DeriveEmptySlotBaseNo, 0),
        (DeriveEmptySlotBaseEmpty, 0),
        (DeriveEmptySlotBaseSlot, 1),
        (DeriveSlotBaseNo, 1),
        (DeriveSlotBaseEmpty, 1),
        (DeriveSlotBaseSlot, 2),
    ]
    for c_type, attr_num in expected_res:
        attr_count = 0
        for attr in pdir(c_type()).pattrs:
            if attr.name in [BASE, DERIVE]:
                attr_count += 1
                assert category_match(attr.category, AttrCategory.DESCRIPTOR)
                assert category_match(attr.category, AttrCategory.SLOT)
        assert attr_count == attr_num


def test_set_derive():
    c_types = [DeriveSlotBaseNo, DeriveSlotBaseEmpty, DeriveSlotBaseSlot]
    for c_type in c_types:
        instance = c_type()
        instance.derive = 'foo'
        for attr in pdir(instance).pattrs:
            if attr.name == DERIVE:
                assert category_match(attr.category, AttrCategory.DESCRIPTOR)
                assert category_match(attr.category, AttrCategory.SLOT)
                break
        else:
            # No derive attribute found
            assert False


def test_set_base():
    c_types = [DeriveNoSlotBaseSlot, DeriveEmptySlotBaseSlot, DeriveSlotBaseSlot]
    for c_type in c_types:
        instance = c_type()
        instance.base = 'foo'
        for attr in pdir(instance).pattrs:
            if attr.name == BASE:
                assert category_match(attr.category, AttrCategory.DESCRIPTOR)
                assert category_match(attr.category, AttrCategory.SLOT)
                break
        else:
            # No base attribute found
            assert False
