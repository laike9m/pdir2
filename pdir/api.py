"""
Convention:
"attr" means the original attribute object.
"pattr" means class PrettyAttribute instance.
"""

from __future__ import print_function

import inspect
import platform
from sys import _getframe

from ._internal_utils import category_match, get_dict_attr, is_ptpython
from .attr_category import AttrCategory, get_attr_category
from .constants import dummy_obj, GETTER, SETTER, DELETER
from .format import format_pattrs

if platform.system() == 'Windows':
    from colorama import init

    init()  # To support Windows.


class PrettyDir(object):
    """Class that provides pretty dir and search API."""

    def __init__(self, obj=dummy_obj, pattrs=None):
        """
        Args:
            obj: The object to inspect.
            pattrs: Used when returning search result.
        """
        self.obj = obj
        if pattrs is None:
            attrs = _getframe(1).f_locals if obj is dummy_obj else self._getattr()
            self.dir_result = sorted(list(attrs.keys()))
            self.pattrs = [
                PrettyAttribute(name, get_attr_category(name, attr, obj), attr)
                for name, attr in attrs.items()
            ]
        else:
            self.pattrs = pattrs
            self.dir_result = sorted([p.name for p in pattrs])

    def __repr__(self):
        if is_ptpython():
            print(format_pattrs(self.pattrs), end='')
            return ''
        else:
            return format_pattrs(self.pattrs)

    def __len__(self):
        return len(self.dir_result)

    def __getitem__(self, index):
        return self.dir_result[index]

    def index(self, value):
        return self.dir_result.index(value)

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
                self.obj, [pattr for pattr in self.pattrs if term in pattr.name]
            )
        else:
            term = term.lower()
            return PrettyDir(
                self.obj, [pattr for pattr in self.pattrs if term in pattr.name.lower()]
            )

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
        return PrettyDir(
            self.obj,
            [
                pattr
                for pattr in self.pattrs
                if category_match(pattr.category, AttrCategory.PROPERTY)
            ],
        )

    @property
    def methods(self):
        """Returns all methods of the inspected object.

        Note that "methods" can mean "functions" when inspecting a module.
        """
        return PrettyDir(
            self.obj,
            [
                pattr
                for pattr in self.pattrs
                if category_match(pattr.category, AttrCategory.FUNCTION)
            ],
        )

    @property
    def public(self):
        """Returns public attributes of the inspected object."""
        return PrettyDir(
            self.obj, [pattr for pattr in self.pattrs if not pattr.name.startswith('_')]
        )

    @property
    def own(self):
        """Returns attributes that are not inhterited from parent classes.

        Now we only use a simple judgement, it is expected that many attributes
        not get returned, especially invoked on a module.

        For instance, there's no way to distinguish between properties that
        are initialized in instance class's __init__ and parent class's
        __init__(assuming super() is called). So we'll just leave it.
        """
        return PrettyDir(
            self.obj,
            [
                pattr
                for pattr in self.pattrs
                if pattr.name in type(self.obj).__dict__
                or pattr.name in self.obj.__dict__
            ],
        )

    def _getattr(self):
        """A wrapper around getattr(), handling some exceptions."""
        attrs = {}
        for name in dir(self.obj):
            try:
                # Ensures we get descriptor object instead of its return value.
                attrs[name] = get_dict_attr(self.obj, name)
            except AttributeError:
                attrs[name] = getattr(self.obj, name)
        return attrs


class PrettyAttribute(object):
    def __init__(self, name, category, attr_obj):
        self.name = name
        self.category = category
        # Names are grouped by their category. When multiple categories exist,
        # pick the largest one which usually represents a more detailed
        # category.
        self.display_group = max(category) if isinstance(category, tuple) else category
        self.attr_obj = attr_obj
        self.doc = self.get_oneline_doc()
        # single category can not be a bare slot
        self.slotted = (
            AttrCategory.SLOT in self.category if isinstance(category, tuple) else False
        )

    def __repr__(self):
        return '%s: %s' % (self.name, self.category)

    def get_oneline_doc(self):
        """
        Doc doesn't necessarily mean doctring. It could be anything that
        should be put after the attr's name as an explanation.
        """
        attr = self.attr_obj
        if self.display_group == AttrCategory.DESCRIPTOR:
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
