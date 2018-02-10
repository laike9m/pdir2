import collections
import inspect
from os.path import expanduser
from sys import modules

from enum import IntEnum

from .utils import Incrementer


class _SkippedAttribute(object):
    pass


skipped_attribute = _SkippedAttribute()
default_obj = skipped_attribute  # reuse!


class AttrType(object):
    def __init__(self, *categories):
        self.categories = frozenset(categories)
        self.max_category = max(categories)

    def __eq__(self, other):
        if isinstance(other, AttrCategory):
            return other in self.categories
        elif isinstance(other, AttrType):
            return other.categories == self.categories
        else:
            raise TypeError('AttrCategory can\'t be compared with %s' %
                            type(other))

    def __lt__(self, other):
        """For sorting attrs by max_category in output."""
        return str(self.max_category) < str(other.max_category)


# Uses IntEnum so that we can directly compare AttrCategory objects.
# Detailed categories are guaranteed to have large value, so
# AttrType.max_category will always choose detailed category instead of
# basic category.
class AttrCategory(IntEnum):
    # Basic category.
    CLASS = Incrementer.auto()
    # Often represents the internal function that's invoked: add -> __add__.
    FUNCTION = Incrementer.auto()
    EXCEPTION = Incrementer.auto()
    PROPERTY = Incrementer.auto()

    # Detailed category.
    MODULE_ATTRIBUTE = Incrementer.auto()
    SPECIAL_ATTRIBUTE = Incrementer.auto()
    ABSTRACT_CLASS = Incrementer.auto()
    MAGIC = Incrementer.auto()
    ARITHMETIC = Incrementer.auto()
    ITER = Incrementer.auto()
    CONTEXT_MANAGER = Incrementer.auto()
    OBJECT_CUSTOMIZATION = Incrementer.auto()
    RICH_COMPARISON = Incrementer.auto()
    ATTRIBUTE_ACCESS = Incrementer.auto()
    DESCRIPTOR = Incrementer.auto()
    DESCRIPTOR_CLASS = Incrementer.auto()
    CLASS_CUSTOMIZATION = Incrementer.auto()
    CONTAINER = Incrementer.auto()
    COUROUTINE = Incrementer.auto()
    COPY = Incrementer.auto()
    PICKLE = Incrementer.auto()

    def __str__(self):
        """
        e.g. RICH_COMPARISON -> rich comparison
        """
        return ' '.join(self.name.split('_')).lower()


# There are always exceptions, aka attributes cannot be accessed by getattr.
# They are recorded here, along with the type/class of their host objects.
ATTR_EXCEPTION_MAP = {
    "<type 'spacy.tokens.token.Token'>": {
        'has_repvec': skipped_attribute,
        'repvec': skipped_attribute,
    },
    "<class 'pandas.core.frame.DataFrame'>": {
        'columns': None,  # DEFAULT_CATEGORY.
        'index': None,
    },
    "<type 'type'>": {  # py2
        '__abstractmethods__': None,  # ABSTRACT_CLASS.
    },
    "<class 'type'>":
    {  # py3
        '__abstractmethods__': None,  # ABSTRACT_CLASS.
    }
}


def always_true(obj):
    return True


# Second level
ATTR_MAP = {
    '__doc__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__qualname__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__module__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__defaults__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__code__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__globals__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__dict__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__closure__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__annotations__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__kwdefaults__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__func__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__self__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__bases__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__class__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__objclass__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__slots__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__weakref__':
    AttrType(AttrCategory.SPECIAL_ATTRIBUTE, AttrCategory.PROPERTY),
    '__next__':
    AttrType(AttrCategory.ITER, AttrCategory.FUNCTION),
    '__reversed__': [
        (lambda obj: isinstance(obj, collections.Iterator),
         AttrType(AttrCategory.ITER, AttrCategory.FUNCTION), ),
        (always_true, AttrType(AttrCategory.CONTAINER,
                               AttrCategory.FUNCTION), ),
    ],
    '__iter__': [
        (lambda obj: isinstance(obj, collections.Iterator),
         AttrType(AttrCategory.ITER, AttrCategory.FUNCTION), ),
        (always_true, AttrType(AttrCategory.CONTAINER,
                               AttrCategory.FUNCTION), ),
    ],
    '__enter__':
    AttrType(AttrCategory.CONTEXT_MANAGER, AttrCategory.FUNCTION),
    '__exit__':
    AttrType(AttrCategory.CONTEXT_MANAGER, AttrCategory.FUNCTION),
    '__name__':
    [(lambda obj: inspect.ismodule(obj),
      AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY), ),
     (always_true, AttrType(AttrCategory.SPECIAL_ATTRIBUTE,
                            AttrCategory.PROPERTY))],
    '__loader__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__package__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__spec__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__path__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__file__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__cached__':
    AttrType(AttrCategory.MODULE_ATTRIBUTE, AttrCategory.PROPERTY),
    '__abs__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__add__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__and__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__complex__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__divmod__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__float__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__floordiv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__iadd__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__iand__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ifloordiv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ilshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imatmul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imod__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__imul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__int__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__invert__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ior__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ipow__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__irshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__isub__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__itruediv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ixor__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__lshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__matmul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__mod__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__mul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__neg__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__or__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__pos__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__pow__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__radd__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rand__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rdivmod__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rfloordiv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rlshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmatmul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmod__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rmul__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ror__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__round__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rpow__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rrshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rshift__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rsub__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rtruediv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__rxor__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__sub__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__truediv__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__xor__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__ceil__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__floor__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__trunc__':
    AttrType(AttrCategory.ARITHMETIC, AttrCategory.FUNCTION),
    '__init__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__new__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__del__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__repr__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__str__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__bytes__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__format__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__hash__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__bool__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__sizeof__':
    AttrType(AttrCategory.OBJECT_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__lt__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__le__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__eq__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__ne__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__gt__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__ge__':
    AttrType(AttrCategory.RICH_COMPARISON, AttrCategory.FUNCTION),
    '__getattr__':
    AttrType(AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__getattribute__':
    AttrType(AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__setattr__':
    AttrType(AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__delattr__':
    AttrType(AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__dir__':
    AttrType(AttrCategory.ATTRIBUTE_ACCESS, AttrCategory.FUNCTION),
    '__get__':
    AttrType(AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__set__':
    AttrType(AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__delete__':
    AttrType(AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__set_name__':
    AttrType(AttrCategory.DESCRIPTOR_CLASS, AttrCategory.FUNCTION),
    '__init_subclass__':
    AttrType(AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__prepare__':
    AttrType(AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__instancecheck__':
    AttrType(AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__subclasscheck__':
    AttrType(AttrCategory.CLASS_CUSTOMIZATION, AttrCategory.FUNCTION),
    '__subclasshook__':
    AttrType(AttrCategory.ABSTRACT_CLASS, AttrCategory.FUNCTION),
    '__isabstractmethod__':
    AttrType(AttrCategory.ABSTRACT_CLASS, AttrCategory.FUNCTION),
    '__abstractmethods__':
    AttrType(AttrCategory.ABSTRACT_CLASS, AttrCategory.PROPERTY),
    '__len__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__length_hint__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__getitem__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__missing__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__setitem__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__delitem__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__contains__':
    AttrType(AttrCategory.CONTAINER, AttrCategory.FUNCTION),
    '__await__':
    AttrType(AttrCategory.COUROUTINE, AttrCategory.FUNCTION),
    '__aiter__':
    AttrType(AttrCategory.COUROUTINE, AttrCategory.FUNCTION),
    '__anext__':
    AttrType(AttrCategory.COUROUTINE, AttrCategory.FUNCTION),
    '__aenter__':
    AttrType(AttrCategory.COUROUTINE, AttrCategory.FUNCTION),
    '__aexit__':
    AttrType(AttrCategory.COUROUTINE, AttrCategory.FUNCTION),
    '__index__':
    AttrType(AttrCategory.MAGIC, AttrCategory.FUNCTION),
    '__call__':
    AttrType(AttrCategory.MAGIC, AttrCategory.FUNCTION),
    '__copy__':
    AttrType(AttrCategory.COPY, AttrCategory.FUNCTION),
    '__deepcopy__':
    AttrType(AttrCategory.COPY, AttrCategory.FUNCTION),
    '__getnewargs_ex__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__getnewargs__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__getstate__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__setstate__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__reduce__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
    '__reduce_ex__':
    AttrType(AttrCategory.PICKLE, AttrCategory.FUNCTION),
}

# repl
PYTHON = 'python'
IPYTHON = 'ipython'
PTPYTHON = 'ptpython'
BPYTHON = 'bpython'

# descriptor
GETTER = 'getter'
SETTER = 'setter'
DELETER = 'deleter'
method_descriptor = type(list.append)


def _get_repl_type():
    if any('ptpython' in key for key in modules):
        return PTPYTHON
    if any('bpython' in key for key in modules):
        return BPYTHON
    try:
        __IPYTHON__
        return IPYTHON
    except NameError:
        return PYTHON


repl_type = _get_repl_type()

# Color
BLACK = 'black'
BRIGHT_BLACK = 'bright black'
GREY = 'grey'
RED = 'red'
BRIGHT_RED = 'bright red'
GREEN = 'green'
BRIGHT_GREEN = 'bright green'
YELLOW = 'yellow'
BRIGHT_YELLOW = 'bright yellow'
BLUE = 'blue'
BRIGHT_BLUE = 'bright blue'
MAGENTA = 'magenta'
BRIGHT_MAGENTA = 'bright magenta'
CYAN = 'cyan'
BRIGHT_CYAN = 'bright cyan'
WHITE = 'white'
BRIGHT_WHITE = 'bright white'
VALID_COLORS = frozenset({
    BLACK, BRIGHT_BLACK, RED, BRIGHT_RED, GREEN, BRIGHT_GREEN, YELLOW,
    BRIGHT_YELLOW, BLUE, BRIGHT_BLUE, MAGENTA, BRIGHT_MAGENTA, CYAN,
    BRIGHT_CYAN, WHITE, BRIGHT_WHITE
})

# User Configuration
DEFAULT_CONFIG_FILE = expanduser('~/.pdir2config')
CONFIG_FILE_ENV = 'PDIR2_CONFIG_FILE'
DEFAULT = 'global'
UNIFORM_COLOR = 'uniform-color'
CATEGORY_COLOR = 'category-color'
ATTRIBUTE_COLOR = 'attribute-color'
COMMA_COLOR = 'comma-color'
DOC_COLOR = 'doc-color'
VALID_CONFIG_KEYS = frozenset(
    {UNIFORM_COLOR, CATEGORY_COLOR, ATTRIBUTE_COLOR, COMMA_COLOR, DOC_COLOR})
