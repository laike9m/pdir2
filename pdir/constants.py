from enum import Enum

dummy_obj = object()


# repl
class ReplType(Enum):
    PYTHON = 'python'
    IPYTHON = 'ipython'
    PTPYTHON = 'ptpython'
    BPYTHON = 'bpython'


# descriptor
GETTER = 'getter'
SETTER = 'setter'
DELETER = 'deleter'


class _ClassWithSlot:
    __slots__ = ['a']


SLOT_TYPE = type(_ClassWithSlot.a)  # type: ignore
