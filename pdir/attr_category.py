import collections.abc
import functools
import inspect
from enum import IntEnum, auto

from ._internal_utils import is_slotted_attr

from typing import Any
from typing import Tuple
from typing import Union


# Detailed category should have larger values than general category.
class AttrCategory(IntEnum):
    # Slot category: orthogonal to all other category
    SLOT = auto()
    # Basic category.
    CLASS = auto()
    # Often represents the internal function that's invoked: add -> __add__.
    FUNCTION = auto()
    EXCEPTION = auto()
    PROPERTY = auto()

    # Detailed category.
    MODULE_ATTRIBUTE = auto()
    SPECIAL_ATTRIBUTE = auto()
    ABSTRACT_CLASS = auto()
    MAGIC = auto()
    ARITHMETIC = auto()
    ITER = auto()
    CONTEXT_MANAGER = auto()
    OBJECT_CUSTOMIZATION = auto()
    RICH_COMPARISON = auto()
    ATTRIBUTE_ACCESS = auto()
    # TODO: We should probably call it "user-defined descriptor", cause pretty much
    # everything inside a class is a "descriptor".
    DESCRIPTOR = auto()
    DESCRIPTOR_CLASS = auto()
    STATIC_METHOD = auto()
    CLASS_CUSTOMIZATION = auto()
    CONTAINER = auto()
    COROUTINE = auto()
    COPY = auto()
    PICKLE = auto()
    PATTERN_MATCHING = auto()
    TYPING = auto()

    def __str__(self) -> str:
        """
        e.g. RICH_COMPARISON -> rich comparison
        """
        return ' '.join(self.name.split('_')).lower()


def _always_true(obj: type) -> bool:
    return True


def category_match(
    pattr_category: Union[Tuple[AttrCategory, ...], AttrCategory],
    target_category: AttrCategory,
) -> bool:
    if pattr_category == target_category:
        return True
    return isinstance(pattr_category, tuple) and target_category in pattr_category


# Names that belong to different categories in different conditions.
ATTR_MAP_CONDITIONAL = {
    '__reversed__': lambda obj: (AttrCategory.ITER, AttrCategory.FUNCTION)
    if isinstance(obj, collections.abc.Iterator)
    else (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__iter__': lambda obj: (AttrCategory.ITER, AttrCategory.FUNCTION)
    if isinstance(obj, collections.abc.Iterator)
    else (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__name__': lambda obj: (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY)
    if inspect.ismodule(obj)
    else (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
}

ATTR_MAP = {
    '__doc__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__qualname__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__module__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__defaults__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__code__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__globals__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__dict__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__closure__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__annotations__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__kwdefaults__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__func__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__self__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__bases__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__class__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__objclass__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__slots__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__weakref__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__excepthook__': (AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__next__': (AttrCategory.ITER, AttrCategory.FUNCTION),
    '__enter__': (AttrCategory.CONTEXT_MANAGER, AttrCategory.FUNCTION),
    '__exit__': (AttrCategory.CONTEXT_MANAGER, AttrCategory.FUNCTION),
    '__loader__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__package__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__spec__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__path__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__file__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__cached__': (AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__abs__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__add__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__and__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__complex__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__divmod__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__float__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__floordiv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__iadd__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__iand__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ifloordiv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ilshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imatmul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imod__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__int__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__invert__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ior__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ipow__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__irshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__isub__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__itruediv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ixor__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__lshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__matmul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__mod__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__mul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__neg__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__or__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__pos__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__pow__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__radd__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rand__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rdivmod__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rfloordiv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rlshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmatmul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmod__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmul__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ror__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__round__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rpow__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rrshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rshift__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rsub__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rtruediv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rxor__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__sub__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__truediv__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__xor__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ceil__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__floor__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__trunc__': (AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__init__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__post_init__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__new__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__del__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__repr__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__str__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__bytes__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__format__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__hash__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__bool__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__sizeof__': (AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__lt__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__le__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__eq__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__ne__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__gt__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__ge__': (AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__getattr__': (AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__getattribute__': (AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__setattr__': (AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__delattr__': (AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__dir__': (AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__get__': (AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__set__': (AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__delete__': (AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__set_name__': (AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__init_subclass__': (AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__prepare__': (AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__instancecheck__': (AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__subclasscheck__': (AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__subclasshook__': (AttrCategory.ABSTRACT_CLASS, AttrCategory.FUNCTION),
    '__isabstractmethod__': (AttrCategory.ABSTRACT_CLASS, AttrCategory.FUNCTION),
    '__abstractmethods__': (AttrCategory.ABSTRACT_CLASS, AttrCategory.PROPERTY),
    '__len__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__length_hint__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__getitem__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__missing__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__setitem__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__delitem__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__contains__': (AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__await__': (AttrCategory.COROUTINE, AttrCategory.FUNCTION),
    '__aiter__': (AttrCategory.COROUTINE, AttrCategory.FUNCTION),
    '__anext__': (AttrCategory.COROUTINE, AttrCategory.FUNCTION),
    '__aenter__': (AttrCategory.COROUTINE, AttrCategory.FUNCTION),
    '__aexit__': (AttrCategory.COROUTINE, AttrCategory.FUNCTION),
    '__index__': (AttrCategory.MAGIC, AttrCategory.FUNCTION),
    '__call__': (AttrCategory.MAGIC, AttrCategory.FUNCTION),
    '__copy__': (AttrCategory.COPY, AttrCategory.FUNCTION),
    '__deepcopy__': (AttrCategory.COPY, AttrCategory.FUNCTION),
    '__getnewargs_ex__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__getnewargs__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__getstate__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__setstate__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__reduce__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__reduce_ex__': (AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__match_args__': (AttrCategory.PATTERN_MATCHING, AttrCategory.PROPERTY),
    '__origin__': (AttrCategory.TYPING, AttrCategory.PROPERTY),
    '__args__': (AttrCategory.TYPING, AttrCategory.PROPERTY),
    '__parameters__': (AttrCategory.TYPING, AttrCategory.PROPERTY),
    '__class_getitem__': (AttrCategory.TYPING, AttrCategory.FUNCTION),
}


def attr_category_postprocess(get_attr_category_func):
    """Unifies attr_category to a tuple, add AttrCategory.SLOT if needed."""

    @functools.wraps(get_attr_category_func)
    def wrapped(name: str, attr: Any, obj: Any) -> Tuple[AttrCategory, ...]:
        category = get_attr_category_func(name, attr, obj)
        category = list(category) if isinstance(category, tuple) else [category]
        if is_slotted_attr(obj, name):
            # Refactoring all tuples to lists is not easy
            # and pleasant. Maybe do this in future if necessary
            category.append(AttrCategory.SLOT)
        return tuple(category)

    return wrapped


@attr_category_postprocess
def get_attr_category(
    name: str, attr: Any, obj: Any
) -> Union[Tuple[AttrCategory, ...], AttrCategory]:
    def is_descriptor(obj: Any) -> bool:
        return (
            hasattr(obj, '__get__')
            or hasattr(obj, '__set__')
            or hasattr(obj, '__delete__')
        )

    method_descriptor = type(list.append)

    if name in ATTR_MAP_CONDITIONAL:
        return ATTR_MAP_CONDITIONAL[name](obj)

    if name in ATTR_MAP:
        return ATTR_MAP[name]

    if inspect.isclass(attr):
        return (
            AttrCategory.EXCEPTION
            if issubclass(attr, Exception)
            else AttrCategory.CLASS
        )
    elif (
        inspect.isfunction(attr)
        or inspect.ismethod(attr)
        or inspect.isbuiltin(attr)
        or isinstance(attr, method_descriptor)
    ):
        # Technically, method_descriptor is descriptor, but since they
        # act as functions, let's treat them as functions.
        return AttrCategory.FUNCTION
    elif isinstance(attr, staticmethod):
        return (
            AttrCategory.DESCRIPTOR,
            AttrCategory.STATIC_METHOD,
            AttrCategory.FUNCTION,
        )
    elif is_descriptor(attr):
        # Maybe add getsetdescriptor memberdescriptor in the future.
        return AttrCategory.DESCRIPTOR, AttrCategory.PROPERTY
    else:
        # attr that is neither function nor class is a normal variable,
        # and it's classified to property.
        return AttrCategory.PROPERTY
