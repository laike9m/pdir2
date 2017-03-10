import collections
import inspect


CLASS = 'class'
DEFAULT_CATEGORY = 'other'
FUNCTION = 'function'

# Attribute
MODULE_ATTRIBUTE = 'module attribute'
SPECIAL_ATTRIBUTE = 'special attribute'

# Function
MAGIC = 'magic method'
ARITHMETIC = 'arithmetic'
ITER = 'iter'
CONTEXT_MANAGER = 'context manager'
OBJECT_CUSTOMIZATION = 'object customization'
RICH_COMPARISON = 'rich comparison'
ATTRIBUTE_ACCESS = 'attribute access'
DESCRIPTOR = 'descriptor'
CLASS_CUSTOMIZATION = 'class customization'
CONTAINER = 'emulating container'
COUROUTINE = 'couroutine'
COPY = 'copy'
PICKLE = 'pickle'


def always_true(obj):
    return True


# Second level
ATTR_MAP = {
    '__doc__': SPECIAL_ATTRIBUTE,
    '__qualname__': SPECIAL_ATTRIBUTE,
    '__module__': SPECIAL_ATTRIBUTE,
    '__defaults__': SPECIAL_ATTRIBUTE,
    '__code__': SPECIAL_ATTRIBUTE,
    '__globals__': SPECIAL_ATTRIBUTE,
    '__dict__': SPECIAL_ATTRIBUTE,
    '__closure__': SPECIAL_ATTRIBUTE,
    '__annotations__': SPECIAL_ATTRIBUTE,
    '__kwdefaults__': SPECIAL_ATTRIBUTE,
    '__func__': SPECIAL_ATTRIBUTE,
    '__self__': SPECIAL_ATTRIBUTE,
    '__bases__': SPECIAL_ATTRIBUTE,
    '__class__': SPECIAL_ATTRIBUTE,
    '__objclass__': SPECIAL_ATTRIBUTE,
    '__slots__': SPECIAL_ATTRIBUTE,
    '__weakref__': SPECIAL_ATTRIBUTE,
    '__next__': ITER,
    '__reversed__': [
        (lambda obj: isinstance(obj, collections.Iterator), ITER),
        (always_true, CONTAINER),
    ],
    '__iter__': [
        (lambda obj: isinstance(obj, collections.Iterator), ITER),
        (always_true, CONTAINER),
    ],
    '__enter__': CONTEXT_MANAGER,
    '__exit__': CONTEXT_MANAGER,
    '__name__': [
        (lambda obj: inspect.ismodule(obj), MODULE_ATTRIBUTE),
        (always_true, SPECIAL_ATTRIBUTE)
    ],
    '__loader__': MODULE_ATTRIBUTE,
    '__package__': MODULE_ATTRIBUTE,
    '__spec__': MODULE_ATTRIBUTE,
    '__path__': MODULE_ATTRIBUTE,
    '__file__': MODULE_ATTRIBUTE,
    '__cached__': MODULE_ATTRIBUTE,
    '__abs__': ARITHMETIC,
    '__add__': ARITHMETIC,
    '__and__': ARITHMETIC,
    '__complex__': ARITHMETIC,
    '__divmod__': ARITHMETIC,
    '__float__': ARITHMETIC,
    '__floordiv__': ARITHMETIC,
    '__iadd__': ARITHMETIC,
    '__iand__': ARITHMETIC,
    '__ifloordiv__': ARITHMETIC,
    '__ilshift__': ARITHMETIC,
    '__imatmul__': ARITHMETIC,
    '__imod__': ARITHMETIC,
    '__imul__': ARITHMETIC,
    '__int__': ARITHMETIC,
    '__invert__': ARITHMETIC,
    '__ior__': ARITHMETIC,
    '__ipow__': ARITHMETIC,
    '__irshift__': ARITHMETIC,
    '__isub__': ARITHMETIC,
    '__itruediv__': ARITHMETIC,
    '__ixor__': ARITHMETIC,
    '__lshift__': ARITHMETIC,
    '__matmul__': ARITHMETIC,
    '__mod__': ARITHMETIC,
    '__mul__': ARITHMETIC,
    '__neg__': ARITHMETIC,
    '__or__': ARITHMETIC,
    '__pos__': ARITHMETIC,
    '__pow__': ARITHMETIC,
    '__radd__': ARITHMETIC,
    '__rand__': ARITHMETIC,
    '__rdivmod__': ARITHMETIC,
    '__rfloordiv__': ARITHMETIC,
    '__rlshift__': ARITHMETIC,
    '__rmatmul__': ARITHMETIC,
    '__rmod__': ARITHMETIC,
    '__rmul__': ARITHMETIC,
    '__ror__': ARITHMETIC,
    '__round__': ARITHMETIC,
    '__rpow__': ARITHMETIC,
    '__rrshift__': ARITHMETIC,
    '__rshift__': ARITHMETIC,
    '__rsub__': ARITHMETIC,
    '__rtruediv__': ARITHMETIC,
    '__rxor__': ARITHMETIC,
    '__sub__': ARITHMETIC,
    '__truediv__': ARITHMETIC,
    '__xor__': ARITHMETIC,
    '__ceil__': ARITHMETIC,
    '__floor__': ARITHMETIC,
    '__trunc__': ARITHMETIC,
    '__init__': OBJECT_CUSTOMIZATION,
    '__new__': OBJECT_CUSTOMIZATION,
    '__del__': OBJECT_CUSTOMIZATION,
    '__repr__': OBJECT_CUSTOMIZATION,
    '__str__': OBJECT_CUSTOMIZATION,
    '__bytes__': OBJECT_CUSTOMIZATION,
    '__format__': OBJECT_CUSTOMIZATION,
    '__hash__': OBJECT_CUSTOMIZATION,
    '__bool__': OBJECT_CUSTOMIZATION,
    '__sizeof__': OBJECT_CUSTOMIZATION,
    '__lt__': RICH_COMPARISON,
    '__le__': RICH_COMPARISON,
    '__eq__': RICH_COMPARISON,
    '__ne__': RICH_COMPARISON,
    '__gt__': RICH_COMPARISON,
    '__ge__': RICH_COMPARISON,
    '__getattr__': ATTRIBUTE_ACCESS,
    '__getattribute__': ATTRIBUTE_ACCESS,
    '__setattr__': ATTRIBUTE_ACCESS,
    '__delattr__': ATTRIBUTE_ACCESS,
    '__dir__': ATTRIBUTE_ACCESS,
    '__get__': DESCRIPTOR,
    '__set__': DESCRIPTOR,
    '__delete__': DESCRIPTOR,
    '__set_name__': DESCRIPTOR,
    '__init_subclass__': CLASS_CUSTOMIZATION,
    '__prepare__': CLASS_CUSTOMIZATION,
    '__instancecheck__': CLASS_CUSTOMIZATION,
    '__subclasscheck__': CLASS_CUSTOMIZATION,
    '__subclasshook__': CLASS_CUSTOMIZATION,
    '__len__': CONTAINER,
    '__length_hint__': CONTAINER,
    '__getitem__': CONTAINER,
    '__missing__': CONTAINER,
    '__setitem__': CONTAINER,
    '__delitem__': CONTAINER,
    '__contains__': CONTAINER,
    '__await__': COUROUTINE,
    '__aiter__': COUROUTINE,
    '__anext__': COUROUTINE,
    '__aenter__': COUROUTINE,
    '__aexit__': COUROUTINE,
    '__index__': MAGIC,
    '__call__': MAGIC,
    '__copy__': COPY,
    '__deepcopy__': COPY,
    '__getnewargs_ex__': PICKLE,
    '__getnewargs__': PICKLE,
    '__getstate__': PICKLE,
    '__setstate__': PICKLE,
    '__reduce__': PICKLE,
    '__reduce_ex__': PICKLE,
}


class Color(object):
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def wrap_text(self, text):
        return self.content % text


white = Color('white', '\033[0;37m%s\033[0;m')
green = Color('green', '\033[0;32m%s\033[0;m')
red = Color('red', '\033[0;31m%s\033[0;m')
grey = Color('grey', '\033[1;30m%s\033[0;m')
yellow = Color('yellow', '\033[0;33m%s\033[0;m')
cyan = Color('cyan', '\033[0;36m%s\033[0;m')
comma = grey.wrap_text(', ')
