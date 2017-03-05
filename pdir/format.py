"""
1. group name color
2. attr color
3. how attr is organized(one-line/multi-line, has doc)
"""
from enum import Enum
from colorama import init
try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch

from .constants import *


init()  # To support Windows.


class AttributeFormatterType(Enum):
    """Use this so we can have groups for attribute categorys."""
    SINGLE_LINE = 1
    MULTILINE_WITH_DOC = 2


@singledispatch
def format_attrs_of_a_category(formatter_type, category, attrs):
    category_line = yellow.wrap_text(category) + ':'
    return '%s\n    %s' % (category_line, comma.join(
        cyan.wrap_text(attr.name) for attr in attrs))


@format_attrs_of_a_category.register(AttributeFormatterType.MULTILINE_WITH_DOC)
def _(formatter_type, category, attrs):
    category_line = yellow.wrap_text(category) + ':\n'
    return category_line + '\n'.join('    %s: %s' % (
        cyan.wrap_text(attr.name), grey.wrap_text(attr.doc)) for attr in attrs)


CATEGORY_FORMAT_TABLE = {
    DEFAULT_CATEGORY: AttributeFormatterType.SINGLE_LINE,
    FUNCTION: AttributeFormatterType.MULTILINE_WITH_DOC,
    CLASS: AttributeFormatterType.MULTILINE_WITH_DOC,
    # Attribute
    MODULE_ATTRIBUTE: AttributeFormatterType.SINGLE_LINE,
    SPECIAL_ATTRIBUTE: AttributeFormatterType.MULTILINE_WITH_DOC,
    # Function
    MAGIC: AttributeFormatterType.MULTILINE_WITH_DOC,
    ARITHMETIC: AttributeFormatterType.SINGLE_LINE,
    ITER: AttributeFormatterType.SINGLE_LINE,
    CONTEXT_MANAGER: AttributeFormatterType.SINGLE_LINE,
    OBJECT_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    RICH_COMPARISON: AttributeFormatterType.SINGLE_LINE,
    ATTRIBUTE_ACCESS: AttributeFormatterType.SINGLE_LINE,
    DESCRIPTOR: AttributeFormatterType.SINGLE_LINE,
    CLASS_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    CONTAINER: AttributeFormatterType.SINGLE_LINE,
    COUROUTINE: AttributeFormatterType.SINGLE_LINE,
    COPY: AttributeFormatterType.SINGLE_LINE,
    PICKLE: AttributeFormatterType.SINGLE_LINE,
}


def format_category(category, attrs):
    """Generate repr for attrs of a category."""
    return format_attrs_of_a_category(CATEGORY_FORMAT_TABLE[category],
                                      category, attrs)
