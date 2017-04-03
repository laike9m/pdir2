"""
Defines how attr is organized and displayed.
"""
from enum import Enum

from .constants import *
from .configuration import cfg

if cfg.uniform_color:
    category_color = attribute_color = doc_color = cfg.uniform_color
    comma = cfg.uniform_color.wrap_text(', ')
else:
    category_color = cfg.category_color
    attribute_color = cfg.attribute_color
    doc_color = cfg.doc_color
    comma = cfg.comma_color.wrap_text(', ')


def format_single_line(category, attrs):
    category_line = category_color.wrap_text(category + ':')
    return '{0}\n    {1}'.format(
        category_line,
        comma.join(attribute_color.wrap_text(attr.name) for attr in attrs))


def format_multiline_with_doc(category, attrs):
    category_line = category_color.wrap_text(category + ':') + '\n'
    return category_line + '\n'.join(
        '    {0} {1}'.format(attribute_color.wrap_text(attr.name + ':'),
                             doc_color.wrap_text(attr.doc))
        for attr in attrs)


def format_descriptor(category, attrs):
    """
    Currently it's the same as multi-line doc mode.
    """
    category_line = category_color.wrap_text(category + ':') + '\n'
    return category_line + '\n'.join(
        '    {0} {1}'.format(attribute_color.wrap_text(attr.name + ':'),
                             doc_color.wrap_text(attr.doc))
        for attr in attrs)


class AttributeFormatterType(Enum):
    """Use this so we can have groups for attribute categorys."""
    SINGLE_LINE = (0, format_single_line)
    DESCRIPTOR = (1, format_descriptor)
    MULTILINE_WITH_DOC = (2, format_multiline_with_doc)


CATEGORY_FORMAT_TABLE = {
    DEFAULT_CATEGORY: AttributeFormatterType.SINGLE_LINE,
    FUNCTION: AttributeFormatterType.MULTILINE_WITH_DOC,
    CLASS: AttributeFormatterType.MULTILINE_WITH_DOC,
    EXCEPTION: AttributeFormatterType.MULTILINE_WITH_DOC,
    # Attribute
    MODULE_ATTRIBUTE: AttributeFormatterType.SINGLE_LINE,
    SPECIAL_ATTRIBUTE: AttributeFormatterType.SINGLE_LINE,
    # Function
    MAGIC: AttributeFormatterType.MULTILINE_WITH_DOC,
    ARITHMETIC: AttributeFormatterType.SINGLE_LINE,
    ITER: AttributeFormatterType.SINGLE_LINE,
    CONTEXT_MANAGER: AttributeFormatterType.SINGLE_LINE,
    OBJECT_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    RICH_COMPARISON: AttributeFormatterType.SINGLE_LINE,
    ATTRIBUTE_ACCESS: AttributeFormatterType.SINGLE_LINE,
    DESCRIPTOR: AttributeFormatterType.DESCRIPTOR,
    DESCRIPTOR_CLASS: AttributeFormatterType.SINGLE_LINE,
    CLASS_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    CONTAINER: AttributeFormatterType.SINGLE_LINE,
    COUROUTINE: AttributeFormatterType.SINGLE_LINE,
    COPY: AttributeFormatterType.SINGLE_LINE,
    PICKLE: AttributeFormatterType.SINGLE_LINE,
    ABSTRACT_CLASS: AttributeFormatterType.SINGLE_LINE,
}


def format_category(category, attrs):
    """Generate repr for attrs of a category."""
    formatter_index, formatter = CATEGORY_FORMAT_TABLE[category].value
    return formatter_index, formatter(category, attrs)
