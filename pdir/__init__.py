import sys
from .api import PrettyDir

__author__ = 'laike9m <laike9m@gmail.com>'

sys.modules[__name__] = PrettyDir  # type: ignore
