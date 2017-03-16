"""
1. group name color
2. attr color
3. how attr is organized(one-line/multi-line, has doc)
"""
from enum import Enum

from .constants import *


class Color(object):
    def __init__(self, name, color_code, intensity='0'):
        self.name = name
        self.color_code = color_code
        self.intensity = intensity

    def wrap_text(self, text):
        if repl_type == BPYTHON:
            colored_text = '\033[%sm%s\033[0m' % (self.color_code, text)
            if self.intensity == '0':
                return colored_text
            else:
                return '\033[1m' + colored_text
        else:
            return '\033[%s;%sm%s\033[0;m' % (self.intensity, self.color_code,
                                              text)


white = Color('white', '37')
green = Color('green', '32')
red = Color('red', '31')
grey = Color('grey', '30', '1')
yellow = Color('yellow', '33')
cyan = Color('cyan', '36')
comma = grey.wrap_text(', ')


class AttributeFormatterType(Enum):
    """Use this so we can have groups for attribute categorys."""
    SINGLE_LINE = 1
    MULTILINE_WITH_DOC = 2


def format_single_line(category, attrs):
    category_line = yellow.wrap_text(category + ':')
    return '{0}\n    {1}'.format(
        category_line,
        comma.join(cyan.wrap_text(attr.name) for attr in attrs))


def format_multiline_with_doc(category, attrs):
    category_line = yellow.wrap_text(category + ':') + '\n'
    return category_line + '\n'.join(
        '    {0} {1}'.format(cyan.wrap_text(attr.name + ':'),
                             grey.wrap_text(attr.doc))
        for attr in attrs)


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
    DESCRIPTOR: AttributeFormatterType.SINGLE_LINE,
    CLASS_CUSTOMIZATION: AttributeFormatterType.SINGLE_LINE,
    CONTAINER: AttributeFormatterType.SINGLE_LINE,
    COUROUTINE: AttributeFormatterType.SINGLE_LINE,
    COPY: AttributeFormatterType.SINGLE_LINE,
    PICKLE: AttributeFormatterType.SINGLE_LINE,
}


def format_category(category, attrs):
    """Generate repr for attrs of a category."""
    formatter_type = CATEGORY_FORMAT_TABLE[category]
    if formatter_type == AttributeFormatterType.MULTILINE_WITH_DOC:
        return formatter_type.value, format_multiline_with_doc(category, attrs)
    else:
        return formatter_type.value, format_single_line(category, attrs)
