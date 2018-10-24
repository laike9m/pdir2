import sys

from .constants import ReplType, SLOT_TYPE


# Modified from http://stackoverflow.com/a/3681323/2142577.
def get_dict_attr(attr_obj, attr_name):
    for obj in [attr_obj] + list(attr_obj.__class__.__mro__):
        if hasattr(obj, '__dict__') and attr_name in obj.__dict__:
            return obj.__dict__[attr_name]
    raise AttributeError


def is_slotted_attr(child_obj, attr_name):
    for obj in list(child_obj.__class__.__mro__):
        if isinstance(getattr(obj, attr_name, None), SLOT_TYPE):
            return True
    return False


class Incrementer(object):
    """Class that generates incremental int values.

    auto() in enum/aenum module is not guaranteed to generate incremental
    values, that's why this class is needed.
    """

    __value = -1

    @classmethod
    def auto(cls):
        cls.__value += 1
        return cls.__value


def category_match(pattr_category, target_category):
    if pattr_category == target_category:
        return True
    return isinstance(pattr_category, tuple) and target_category in pattr_category


def _get_repl_type():
    if any(ReplType.PTPYTHON.value in key for key in sys.modules):
        return ReplType.PTPYTHON
    if any(ReplType.BPYTHON.value in key for key in sys.modules):
        return ReplType.BPYTHON
    try:
        __IPYTHON__
        return ReplType.IPYTHON
    except NameError:
        return ReplType.PYTHON


def is_bpython():
    return _get_repl_type() == ReplType.BPYTHON


def is_ptpython():
    return _get_repl_type() == ReplType.PTPYTHON
