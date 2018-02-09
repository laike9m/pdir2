# Tests AttrType's behaviors.

from pdir.constants import AttrType, AttrCategory


def test_attrtype_equality():
    at1 = AttrType(AttrCategory.FUNCTION, AttrCategory.CLASS)
    at2 = AttrType(AttrCategory.FUNCTION, AttrCategory.CLASS)
    at3 = AttrType(AttrCategory.FUNCTION)
    assert at1 == at2
    assert at1 != at3
    assert at1 == AttrCategory.FUNCTION
    assert at1 == AttrCategory.CLASS


def test_attrtype_compare():
    assert (AttrType(AttrCategory.CLASS) <
            AttrType(AttrCategory.FUNCTION))
    assert (AttrType(AttrCategory.FUNCTION, AttrCategory.ARITHMETIC) <
            AttrType(AttrCategory.FUNCTION, AttrCategory.DESCRIPTOR))
