import sys
import inspect

from .constants import ReplType, SLOT_TYPE


def get_attr_from_dict(inspected_obj, attr_name):
    """Ensures we get descriptor object instead of its return value.
    """
    if inspect.isclass(inspected_obj):
        obj_list = [inspected_obj] + list(inspected_obj.__mro__)
    else:
        obj_list = [inspected_obj] + list(inspected_obj.__class__.__mro__)
    for obj in obj_list:
        if hasattr(obj, '__dict__') and attr_name in obj.__dict__:
            return obj.__dict__[attr_name]
    # This happens when user-defined __dir__ returns something that's not
    # in any __dict__. See test_override_dir.
    # Returns attr_name so that it's treated as a normal property.
    return attr_name


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
