"""
Convention:
"attr" means the original attribute object.
"pattr" means class PrettyAttribute instance.
"""

from __future__ import print_function

import inspect
import platform
from sys import _getframe
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from ._internal_utils import get_attr_from_dict, is_ptpython
from .attr_category import AttrCategory, get_attr_category, category_match
from .constants import dummy_obj, GETTER, SETTER, DELETER
from . import format

if platform.system() == 'Windows':
    from colorama import init

    init()  # To support Windows.


class PrettyDir:
    """Class that provides pretty dir and search API."""

    def __init__(
        self, obj: Any = dummy_obj, pattrs: Optional[List['PrettyAttribute']] = None
    ) -> None:
        """
        Args:
            obj: The object to inspect.
            pattrs: Used when returning search result.
        """
        self.obj = obj
        if pattrs is None:
            if obj is dummy_obj:
                # User is calling dir() without arguments.
                attrs = _getframe(1).f_locals
                self.dir_result = sorted(list(attrs.keys()))
            else:
                self.dir_result = dir(self.obj)
                attrs = {
                    name: get_attr_from_dict(self.obj, name) for name in self.dir_result
                }
            self.pattrs = [
                PrettyAttribute(name, get_attr_category(name, attr, obj), attr)
                for name, attr in attrs.items()
            ]
        else:
            self.pattrs = pattrs
            self.dir_result = sorted([p.name for p in pattrs])

    def __repr__(self) -> str:
        if not is_ptpython():
            return format.format_pattrs(self.pattrs)

        print(format.format_pattrs(self.pattrs), end='')
        return ''

    def __len__(self) -> int:
        return len(self.dir_result)

    def __getitem__(self, index: int) -> str:
        return self.dir_result[index]

    def index(self, value):
        return self.dir_result.index(value)

    def search(self, term: str, case_sensitive: bool = False) -> 'PrettyDir':
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
    def properties(self) -> 'PrettyDir':
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
    def methods(self) -> 'PrettyDir':
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
    def public(self) -> 'PrettyDir':
        """Returns public attributes of the inspected object."""
        return PrettyDir(
            self.obj, [pattr for pattr in self.pattrs if not pattr.name.startswith('_')]
        )

    @property
    def own(self) -> 'PrettyDir':
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


class PrettyAttribute:
    def __init__(
        self, name: str, category: Tuple[AttrCategory, ...], attr_obj: Any
    ) -> None:
        self.name = name
        self.category = category
        # Names are grouped by their category. When multiple categories exist,
        # pick the largest one which usually represents a more detailed
        # category.
        self.display_group = max(category)
        self.attr_obj = attr_obj
        self.doc = self.get_oneline_doc()
        # single category can not be a bare slot
        self.slotted = AttrCategory.SLOT in self.category

    def __repr__(self):
        return '%s: %s' % (self.name, self.category)

    def get_oneline_doc(self) -> str:
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
            doc = inspect.getdoc(attr)
            if doc is not None:
                doc_list.append(doc.split('\n', 1)[0])
            return ', '.join(doc_list)

        try:
            hasattr_doc = hasattr(attr, '__doc__')
        except:
            hasattr_doc = False

        if hasattr_doc:
            doc = inspect.getdoc(attr)
            return doc.split('\n', 1)[0] if doc else ''  # default doc is None
        return ''
