"""
TODO:
1. Cache
same object(same id), check source, update
return cached object, meta programming?(p2)
4. config color(p2)
5. colorful docstring(p1)
"""

import inspect
from sys import _getframe
from itertools import groupby


from colorama import init

from .constants import ATTR_MAP, CLASS, FUNCTION, DEFAULT_CATEGORY
from .format import format_category

init()  # To support Windows.


class PrettyDir(object):
    def __init__(self, obj=None):
        self.object = obj
        self.source = dir(obj) if obj else _getframe(1).f_locals
        self.attrs = []
        self.__inspect_category()

    @staticmethod
    def get_oneline_doc(attribute):
        if hasattr(attribute, '__doc__'):
            doc = inspect.getdoc(attribute)
            return doc.split('\n', 1)[0] if doc else ''  # default doc is None
        return None

    def __repr__(self):
        output = []
        for category, attrs in groupby(self.attrs, lambda x: x.category):
            output.append(format_category(category, attrs))

        output.sort(key=lambda x: x[0])
        return '\n'.join(category_output[1] for category_output in output)

    def __inspect_category(self):
        for name in self.source:
            if self.object:
                attribute = getattr(self.object, name)
            else:
                attribute = self.source[name]
            category = ATTR_MAP.get(name, self.get_category(attribute))
            if isinstance(category, list):
                for selector, real_category in category:
                    if selector(self.object):
                        category = real_category
                        break
                else:
                    raise ValueError('category not match: ' + name)
            doc = self.get_oneline_doc(attribute)
            self.attrs.append(PrettyAttribute(name, category, doc))

        self.attrs.sort(key=lambda x: x.category)

    @staticmethod
    def get_category(attribute):
        if inspect.isclass(attribute):
            return CLASS
        elif inspect.isfunction(attribute):
            return FUNCTION
        elif inspect.isbuiltin(attribute):
            return FUNCTION
        elif inspect.ismethoddescriptor(attribute):  # list.append
            return FUNCTION
        else:
            return DEFAULT_CATEGORY


class PrettyAttribute(object):
    def __init__(self, name, category, doc=None):
        self.name = name
        self.category = category
        self.doc = doc
