import sys

from .constants import ReplType


# Copied from http://stackoverflow.com/a/3681323/2142577.
def get_dict_attr(obj, attr):
    for obj in [obj] + list(obj.__class__.__mro__):
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError


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
