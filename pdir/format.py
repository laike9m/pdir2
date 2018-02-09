"""
Defines how attr is organized and displayed.
"""
try:
    from enum import Enum
except ImportError:
    from aenum import Enum

from .configuration import cfg
from .constants import *

if cfg.uniform_color:
    category_color = attribute_color = doc_color = cfg.uniform_color
    comma = cfg.uniform_color.wrap_text(', ')
else:
    category_color = cfg.category_color
    attribute_color = cfg.attribute_color
    doc_color = cfg.doc_color
    comma = cfg.comma_color.wrap_text(', ')


def format_single_line(category, attrs):
    category_line = category_color.wrap_text(str(category) + ':')
    return '{0}\n    {1}'.format(
        category_line,
        comma.join(attribute_color.wrap_text(attr.name) for attr in attrs))


def format_multiline_with_doc(category, attrs):
    category_line = category_color.wrap_text(str(category) + ':') + '\n'
    return category_line + '\n'.join('    {0} {1}'.format(
        attribute_color.wrap_text(attr.name + ':'),
        doc_color.wrap_text(attr.doc)) for attr in attrs)


def format_descriptor(category, attrs):
    """
    Currently it's the same as multi-line doc mode.
    """
    category_line = category_color.wrap_text(str(category) + ':') + '\n'
    return category_line + '\n'.join('    {0} {1}'.format(
        attribute_color.wrap_text(attr.name + ':'),
        doc_color.wrap_text(attr.doc)) for attr in attrs)


class AttributeFormatterType(Enum):
    """Use this so we can have groups for attribute categorys."""
    SINGLE_LINE = (0, format_single_line)
    DESCRIPTOR = (1, format_descriptor)
    MULTILINE_WITH_DOC = (2, format_multiline_with_doc)


CATEGORY_FORMAT_TABLE = {
    AttrCategory.FUNCTION: AttributeFormatterType.MULTILINE_WITH_DOC,
    AttrCategory.CLASS: AttributeFormatterType.MULTILINE_WITH_DOC,
    AttrCategory.EXCEPTION: AttributeFormatterType.MULTILINE_WITH_DOC,
    AttrCategory.PROPERTY: AttributeFormatterType.SINGLE_LINE,
    # Attribute
    AttrCategory.MODULE_ATTRIBUTE: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.SPECIAL_ATTRIBUTE: AttributeFormatterType.SINGLE_LINE,
    # Function
    AttrCategory.MAGIC: AttributeFormatterType.MULTILINE_WITH_DOC,
    AttrCategory.ARITHMETIC: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.ITER: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.CONTEXT_MANAGER: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.OBJECT_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.RICH_COMPARISON: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.ATTRIBUTE_ACCESS: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.DESCRIPTOR: AttributeFormatterType.DESCRIPTOR,
    AttrCategory.DESCRIPTOR_CLASS: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.CLASS_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.CONTAINER: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.COUROUTINE: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.COPY: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.PICKLE: AttributeFormatterType.SINGLE_LINE,
    AttrCategory.ABSTRACT_CLASS: AttributeFormatterType.SINGLE_LINE,
}


def format_category(category, attrs):
    """Generate repr for attrs of a category."""
    formatter_index, formatter = CATEGORY_FORMAT_TABLE[category].value
    return formatter_index, formatter(category, attrs)
