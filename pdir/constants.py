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
