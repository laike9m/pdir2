"""
Convention:
"attr" means the original attribute object.
"pattr" means class PrettyAttribute instance.
"""

from __future__ import print_function

import inspect
import platform
from itertools import groupby
from sys import _getframe

from .constants import *
from .format import format_category
from .utils import get_dict_attr, is_descriptor

if platform.system() == 'Windows':
    from colorama import init
    init()  # To support Windows.


class PrettyDir(object):
    """Class that provides pretty dir and search API."""

    repl_type = repl_type

    def __init__(self, obj=default_obj, pattrs=None):
        """
        Args:
            obj: The object to inspect.
            pattrs: Used when returning search result.
        """
        self.obj = obj
        if pattrs is None:
            self.pattrs = []
            self._sorted_pattrs = None
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
            self.pattrs = pattrs
            self._sorted_pattrs = sorted(pattrs, key=lambda x: x.name)

    def __repr__(self):
        if repl_type == PTPYTHON:
            print(self.repr_str, end='')
            return ''
        else:
            return self.repr_str

    def __len__(self):
        return len(self.pattrs)

    def __getitem__(self, index):
        return self._sorted_pattrs[index].name

    def index(self, value):
        return self._sorted_pattrs.index(value)

    @property
    def repr_str(self):
        output = []
        for category, pattrs in groupby(self.pattrs,
                                        lambda x: x.category.max_category):
            # Format is determined by max_category.
            output.append(format_category(category, pattrs))

        output.sort(key=lambda x: x[0])
        return '\n'.join(category_output[1] for category_output in output)

    def search(self, term, case_sensitive=False):
        """Searches for names that match some pattern.

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
                self.obj,
                [pattr for pattr in self.pattrs if term in pattr.name])
        else:
            term = term.lower()
            return PrettyDir(self.obj, [
                pattr for pattr in self.pattrs if term in pattr.name.lower()
            ])

    s = search

    # Below methods "methods", "public", "own" can be chained when necessary.
    # That is, for listing all public methods that are not inherited,
    # use pdir(obj).public.own.methods
    # The order should not affect results.

    @property
    def properties(self):
        """Returns all properties of the inspected object.

        Note that "properties" can mean "variables".
        """
        return PrettyDir(self.obj, [
            pattr for pattr in self.pattrs
            if pattr.category == AttrCategory.PROPERTY
        ])

    @property
    def methods(self):
        """Returns all methods of the inspected object.

        Note that "methods" can mean "functions" when inspecting a module.
        """
        return PrettyDir(self.obj, [
            pattr for pattr in self.pattrs
            if pattr.category == AttrCategory.FUNCTION
        ])

    @property
    def public(self):
        """Returns public attributes of the inspected object."""
        return PrettyDir(self.obj, [
            pattr for pattr in self.pattrs if not pattr.name.startswith('_')
        ])

    @property
    def own(self):
        """Returns attributes that are not inhterited from parent classes.

        Now we only use a simple judgement, it is expected that many attributes
        not get returned, especially invoked on a module.

        For instance, there's no way to distinguish between properties that
        are initialized in instance class's __init__ and parent class's
        __init__(assuming super() is called). So we'll just leave it.
        """
        return PrettyDir(self.obj, [
            pattr for pattr in self.pattrs
            if pattr.name in type(
                self.obj).__dict__ or pattr.name in self.obj.__dict__
        ])

    def __getattr_wrapper(self, name):
        """A wrapper around getattr(), handling some exceptions."""
        if inspect.isclass(self.obj):
            if name in ATTR_EXCEPTION_MAP.get(str(self.obj), {}):
                return ATTR_EXCEPTION_MAP[str(self.obj)][name]
        elif name in ATTR_EXCEPTION_MAP.get(str(type(self.obj)), {}):
            return ATTR_EXCEPTION_MAP[str(type(self.obj))][name]

        # TODO: use try..except and attach exception message to output.
        try:
            # This is to ensure we get descriptor object instead of
            # its return value.
            return get_dict_attr(self.obj, name)
        except AttributeError:
            return getattr(self.obj, name)

    def __inspect_category(self, source):
        for name, attr in source.items():
            category = ATTR_MAP.get(name, self.get_category(attr))
            if isinstance(category, list):
                for selector, real_category in category:
                    if selector(self.obj):
                        category = real_category
                        break
                else:
                    raise ValueError('category not match: ' + name)
            self.pattrs.append(PrettyAttribute(name, category, attr))

        self.pattrs.sort(key=lambda x: (x.category, x.name))
        self._sorted_pattrs = sorted(self.pattrs, key=lambda x: x.name)

    @staticmethod
    def get_category(attr):
        if inspect.isclass(attr):
            return AttrType(AttrCategory.EXCEPTION) if issubclass(
                attr, Exception) else AttrType(AttrCategory.CLASS)
        elif inspect.isfunction(attr):
            return AttrType(AttrCategory.FUNCTION)
        elif inspect.ismethod(attr):
            return AttrType(AttrCategory.FUNCTION)
        elif inspect.isbuiltin(attr):
            return AttrType(AttrCategory.FUNCTION)
        elif isinstance(attr, method_descriptor):
            # Technically, method_descriptor is descriptor, but since they
            # act as functions, let's treat them as functions.
            return AttrType(AttrCategory.FUNCTION)
        elif is_descriptor(attr):
            # Maybe add getsetdescriptor memberdescriptor in the future.
            return AttrType(AttrCategory.DESCRIPTOR, AttrCategory.PROPERTY)
        else:
            # attr that is neither function nor class is a normal variable,
            # and it's classified to property.
            return AttrType(AttrCategory.PROPERTY)


class PrettyAttribute(object):
    def __init__(self, name, category, attr_obj):
        self.name = name
        self.category = category
        self.attr_obj = attr_obj
        self.doc = self.get_oneline_doc()

    def __repr__(self):
        return '%s: %s' % (self.name, self.category)

    def get_oneline_doc(self):
        """
        Doc doesn't necessarily mean doctring. It could be anything that
        should be put after the attr's name as an explanation.
        """
        attr = self.attr_obj
        if self.category == AttrCategory.DESCRIPTOR:
            if isinstance(attr, property):
                doc_list = ['@property with getter']
                if attr.fset:
                    doc_list.append(SETTER)
                if attr.fdel:
                    doc_list.append(DELETER)
            else:
                doc_list = ['class %s' % attr.__class__.__name__]
                if hasattr(attr, '__get__'):
                    doc_list.append(GETTER)
                if hasattr(attr, '__set__'):
                    doc_list.append(SETTER)
                if hasattr(attr, '__delete__'):
                    doc_list.append(DELETER)
                doc_list[0] = ' '.join([doc_list[0], 'with', doc_list.pop(1)])
            if attr.__doc__ is not None:
                doc_list.append(inspect.getdoc(attr).split('\n', 1)[0])
            return ', '.join(doc_list)

        if hasattr(attr, '__doc__'):
            doc = inspect.getdoc(attr)
            return doc.split('\n', 1)[0] if doc else ''  # default doc is None
        return None
