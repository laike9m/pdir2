import collections
import inspect
from os.path import expanduser
from sys import modules

try:
    from enum import IntEnum
except ImportError:
    from aenum import IntEnum

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
class AttrCategory(IntEnum):
    # Basic category.
    CLASS = Incrementer.auto()
    DEFAULT_CATEGORY = Incrementer.auto()
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
        if self is AttrCategory.DEFAULT_CATEGORY:
            return 'other'
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
    "<class 'type'>": {  # py3
        '__abstractmethods__': None,  # ABSTRACT_CLASS.
    }
}


def always_true(obj):
    return True


# Second level
ATTR_MAP = {
    '__doc__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__qualname__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__module__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__defaults__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__code__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__globals__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__dict__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__closure__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__annotations__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__kwdefaults__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__func__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__self__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__bases__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__class__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__objclass__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__slots__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__weakref__': AttrType(AttrCategory.SPECIAL_ATTRIBUTE,),
    '__next__': AttrType(AttrCategory.ITER,),
    '__reversed__': [
        (lambda obj: isinstance(obj, collections.Iterator),
         AttrType(AttrCategory.ITER),),
        (always_true, AttrType(AttrCategory.CONTAINER),),
    ],
    '__iter__': [
        (lambda obj: isinstance(obj, collections.Iterator),
         AttrType(AttrCategory.ITER),),
        (always_true, AttrType(AttrCategory.CONTAINER),),
    ],
    '__enter__': AttrType(AttrCategory.CONTEXT_MANAGER,),
    '__exit__': AttrType(AttrCategory.CONTEXT_MANAGER,),
    '__name__': [
        (lambda obj: inspect.ismodule(obj),
         AttrType(AttrCategory.MODULE_ATTRIBUTE),),
        (always_true, AttrType(AttrCategory.SPECIAL_ATTRIBUTE))
    ],
    '__loader__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__package__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__spec__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__path__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__file__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__cached__': AttrType(AttrCategory.MODULE_ATTRIBUTE,),
    '__abs__': AttrType(AttrCategory.ARITHMETIC,),
    '__add__': AttrType(AttrCategory.ARITHMETIC,),
    '__and__': AttrType(AttrCategory.ARITHMETIC,),
    '__complex__': AttrType(AttrCategory.ARITHMETIC,),
    '__divmod__': AttrType(AttrCategory.ARITHMETIC,),
    '__float__': AttrType(AttrCategory.ARITHMETIC,),
    '__floordiv__': AttrType(AttrCategory.ARITHMETIC,),
    '__iadd__': AttrType(AttrCategory.ARITHMETIC,),
    '__iand__': AttrType(AttrCategory.ARITHMETIC,),
    '__ifloordiv__': AttrType(AttrCategory.ARITHMETIC,),
    '__ilshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__imatmul__': AttrType(AttrCategory.ARITHMETIC,),
    '__imod__': AttrType(AttrCategory.ARITHMETIC,),
    '__imul__': AttrType(AttrCategory.ARITHMETIC,),
    '__int__': AttrType(AttrCategory.ARITHMETIC,),
    '__invert__': AttrType(AttrCategory.ARITHMETIC,),
    '__ior__': AttrType(AttrCategory.ARITHMETIC,),
    '__ipow__': AttrType(AttrCategory.ARITHMETIC,),
    '__irshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__isub__': AttrType(AttrCategory.ARITHMETIC,),
    '__itruediv__': AttrType(AttrCategory.ARITHMETIC,),
    '__ixor__': AttrType(AttrCategory.ARITHMETIC,),
    '__lshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__matmul__': AttrType(AttrCategory.ARITHMETIC,),
    '__mod__': AttrType(AttrCategory.ARITHMETIC,),
    '__mul__': AttrType(AttrCategory.ARITHMETIC,),
    '__neg__': AttrType(AttrCategory.ARITHMETIC,),
    '__or__': AttrType(AttrCategory.ARITHMETIC,),
    '__pos__': AttrType(AttrCategory.ARITHMETIC,),
    '__pow__': AttrType(AttrCategory.ARITHMETIC,),
    '__radd__': AttrType(AttrCategory.ARITHMETIC,),
    '__rand__': AttrType(AttrCategory.ARITHMETIC,),
    '__rdivmod__': AttrType(AttrCategory.ARITHMETIC,),
    '__rfloordiv__': AttrType(AttrCategory.ARITHMETIC,),
    '__rlshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__rmatmul__': AttrType(AttrCategory.ARITHMETIC,),
    '__rmod__': AttrType(AttrCategory.ARITHMETIC,),
    '__rmul__': AttrType(AttrCategory.ARITHMETIC,),
    '__ror__': AttrType(AttrCategory.ARITHMETIC,),
    '__round__': AttrType(AttrCategory.ARITHMETIC,),
    '__rpow__': AttrType(AttrCategory.ARITHMETIC,),
    '__rrshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__rshift__': AttrType(AttrCategory.ARITHMETIC,),
    '__rsub__': AttrType(AttrCategory.ARITHMETIC,),
    '__rtruediv__': AttrType(AttrCategory.ARITHMETIC,),
    '__rxor__': AttrType(AttrCategory.ARITHMETIC,),
    '__sub__': AttrType(AttrCategory.ARITHMETIC,),
    '__truediv__': AttrType(AttrCategory.ARITHMETIC,),
    '__xor__': AttrType(AttrCategory.ARITHMETIC,),
    '__ceil__': AttrType(AttrCategory.ARITHMETIC,),
    '__floor__': AttrType(AttrCategory.ARITHMETIC,),
    '__trunc__': AttrType(AttrCategory.ARITHMETIC,),
    '__init__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__new__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__del__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__repr__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__str__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__bytes__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__format__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__hash__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__bool__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__sizeof__': AttrType(AttrCategory.OBJECT_CUSTOMIZATION,),
    '__lt__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__le__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__eq__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__ne__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__gt__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__ge__': AttrType(AttrCategory.RICH_COMPARISON,),
    '__getattr__': AttrType(AttrCategory.ATTRIBUTE_ACCESS,),
    '__getattribute__': AttrType(AttrCategory.ATTRIBUTE_ACCESS,),
    '__setattr__': AttrType(AttrCategory.ATTRIBUTE_ACCESS,),
    '__delattr__': AttrType(AttrCategory.ATTRIBUTE_ACCESS,),
    '__dir__': AttrType(AttrCategory.ATTRIBUTE_ACCESS,),
    '__get__': AttrType(AttrCategory.DESCRIPTOR_CLASS,),
    '__set__': AttrType(AttrCategory.DESCRIPTOR_CLASS,),
    '__delete__': AttrType(AttrCategory.DESCRIPTOR_CLASS,),
    '__set_name__': AttrType(AttrCategory.DESCRIPTOR_CLASS,),
    '__init_subclass__': AttrType(AttrCategory.CLASS_CUSTOMIZATION,),
    '__prepare__': AttrType(AttrCategory.CLASS_CUSTOMIZATION,),
    '__instancecheck__': AttrType(AttrCategory.CLASS_CUSTOMIZATION,),
    '__subclasscheck__': AttrType(AttrCategory.CLASS_CUSTOMIZATION,),
    '__subclasshook__': AttrType(AttrCategory.ABSTRACT_CLASS,),
    '__isabstractmethod__': AttrType(AttrCategory.ABSTRACT_CLASS,),
    '__abstractmethods__': AttrType(AttrCategory.ABSTRACT_CLASS,),
    '__len__': AttrType(AttrCategory.CONTAINER,),
    '__length_hint__': AttrType(AttrCategory.CONTAINER,),
    '__getitem__': AttrType(AttrCategory.CONTAINER,),
    '__missing__': AttrType(AttrCategory.CONTAINER,),
    '__setitem__': AttrType(AttrCategory.CONTAINER,),
    '__delitem__': AttrType(AttrCategory.CONTAINER,),
    '__contains__': AttrType(AttrCategory.CONTAINER,),
    '__await__': AttrType(AttrCategory.COUROUTINE,),
    '__aiter__': AttrType(AttrCategory.COUROUTINE,),
    '__anext__': AttrType(AttrCategory.COUROUTINE,),
    '__aenter__': AttrType(AttrCategory.COUROUTINE,),
    '__aexit__': AttrType(AttrCategory.COUROUTINE,),
    '__index__': AttrType(AttrCategory.MAGIC,),
    '__call__': AttrType(AttrCategory.MAGIC,),
    '__copy__': AttrType(AttrCategory.COPY,),
    '__deepcopy__': AttrType(AttrCategory.COPY,),
    '__getnewargs_ex__': AttrType(AttrCategory.PICKLE,),
    '__getnewargs__': AttrType(AttrCategory.PICKLE,),
    '__getstate__': AttrType(AttrCategory.PICKLE,),
    '__setstate__': AttrType(AttrCategory.PICKLE,),
    '__reduce__': AttrType(AttrCategory.PICKLE,),
    '__reduce_ex__': AttrType(AttrCategory.PICKLE,),
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
    BLACK, BRIGHT_BLACK, RED, BRIGHT_RED, GREEN, BRIGHT_GREEN,
    YELLOW, BRIGHT_YELLOW, BLUE, BRIGHT_BLUE, MAGENTA, BRIGHT_MAGENTA,
    CYAN, BRIGHT_CYAN, WHITE, BRIGHT_WHITE})

# User Configuration
DEFAULT_CONFIG_FILE = expanduser('~/.pdir2config')
CONFIG_FILE_ENV = 'PDIR2_CONFIG_FILE'
DEFAULT = 'global'
UNIFORM_COLOR = 'uniform-color'
CATEGORY_COLOR = 'category-color'
ATTRIBUTE_COLOR = 'attribute-color'
COMMA_COLOR = 'comma-color'
DOC_COLOR = 'doc-color'
VALID_CONFIG_KEYS = frozenset({
    UNIFORM_COLOR, CATEGORY_COLOR, ATTRIBUTE_COLOR, COMMA_COLOR, DOC_COLOR})
