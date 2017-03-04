"""
TODO:
1. Cache
same object(same id), check source, update
return cached object, meta programming?(p2)
2. dir() without argument, find correct scope
3. Different categorys have different formatting, e.g.
default magic method in the same line, user defined method each in a line
with one-line doc
4. config color(p2)
"""

import inspect
from itertools import groupby

from .constants import ATTR_MAP, CLASS, FUNCTION, DEFAULT_CATEGORY
from .format import format_category


class PrettyDir(object):
    def __init__(self, obj=None):
        self.object = obj
        if obj is None:
            raise NotImplemented
        else:
            self.source = dir(obj)
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

        return '\n'.join(output)

    def __inspect_category(self):
        for name in self.source:
            attribute = getattr(self.object, name)
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
