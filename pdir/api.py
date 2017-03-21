from __future__ import print_function

import inspect
from itertools import groupby
from sys import _getframe

from colorama import init

from .constants import *
from .format import format_category

init()  # To support Windows.


class PrettyDir(object):
    """Class that provides pretty dir and search API."""

    repl_type = repl_type

    def __init__(self, obj=default_obj, attrs=None):
        """
        Args:
            obj: The object to inspect.
            attrs: Used when returning search result.
        """
        self.obj = obj
        if attrs is None:
            self.attrs = []
            self._sorted_attrs = None
            if obj is default_obj:
                source = _getframe(1).f_locals
            else:
                source = {}
                for name in dir(obj):
                    attr = self.__getattr_wrapper(name)
                    if attr is not skipped_attribute:
                        source[name] = attr
            self.__inspect_category(source)
        else:
            self.attrs = attrs
            self._sorted_attrs = sorted(attrs, key=lambda x: x.name)

    def __repr__(self):
        if repl_type == PTPYTHON:
            print(self.repr_str, end='')
            return ''
        else:
            return self.repr_str

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, index):
        return self._sorted_attrs[index].name

    def index(self, value):
        return self._sorted_attrs.index(value)

    @property
    def repr_str(self):
        output = []
        for category, attrs in groupby(self.attrs, lambda x: x.category):
            output.append(format_category(category, attrs))

        output.sort(key=lambda x: x[0])
        return '\n'.join(category_output[1] for category_output in output)

    def search(self, term, case_sensitive=False):
        """Search for names that match some pattern.

        Args:
            term: String used to match names. A name is returned if it matches
              the whole search term.
            case_sensitive: Boolean to match case or not, default is False
              (case insensitive).

        Return:
            A PrettyDir object with matched names.
        """
        if case_sensitive:
            return PrettyDir(
                self.obj, [attr for attr in self.attrs if term in attr.name])
        else:
            term = term.lower()
            return PrettyDir(self.obj, [
                attr for attr in self.attrs if term in attr.name.lower()
            ])

    s = search

    def __getattr_wrapper(self, name):
        """A wrapper around getattr(), handling some exceptions."""
        if inspect.isclass(self.obj):
            if name in ATTR_EXCEPTION_MAP.get(str(self.obj), {}):
                return ATTR_EXCEPTION_MAP[str(self.obj)][name]
        elif name in ATTR_EXCEPTION_MAP.get(str(type(self.obj)), {}):
            return ATTR_EXCEPTION_MAP[str(type(self.obj))][name]
        else:
            # TODO: use try..except and attach exception message to output.
            return getattr(self.obj, name)

    def __inspect_category(self, source):
        for name, attribute in source.items():
            category = ATTR_MAP.get(name, self.get_category(attribute))
            if isinstance(category, list):
                for selector, real_category in category:
                    if selector(self.obj):
                        category = real_category
                        break
                else:
                    raise ValueError('category not match: ' + name)
            doc = self.get_oneline_doc(attribute)
            self.attrs.append(PrettyAttribute(name, category, doc))

        self.attrs.sort(key=lambda x: (x.category, x.name))
        self._sorted_attrs = sorted(self.attrs, key=lambda x: x.name)

    @staticmethod
    def get_oneline_doc(attribute):
        if hasattr(attribute, '__doc__'):
            doc = inspect.getdoc(attribute)
            return doc.split('\n', 1)[0] if doc else ''  # default doc is None
        return None

    @staticmethod
    def get_category(attribute):
        if inspect.isclass(attribute):
            return EXCEPTION if issubclass(attribute, Exception) else CLASS
        elif inspect.isfunction(attribute):
            return FUNCTION
        elif inspect.ismethod(attribute):
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

    def __repr__(self):
        return '%s: %s' % (self.name, self.category)
