'''
Defines how attr is organized and displayed.
'''
from collections import namedtuple
from itertools import groupby

from .attr_category import AttrCategory
from .configuration import attribute_color, category_color, comma, doc_color


def format_pattrs(pattrs):
    """Generates repr string given a list of pattrs."""
    output = []
    pattrs.sort(
        key=lambda x: (
            _FORMATTER[x.display_group].display_index,
            x.display_group,
            x.name,
        )
    )
    for display_group, grouped_pattrs in groupby(pattrs, lambda x: x.display_group):
        output.append(
            _FORMATTER[display_group].formatter(display_group, grouped_pattrs)
        )

    return '\n'.join(output)


def _format_single_line(category, attrs):
    category_line = category_color.wrap_text(str(category) + ':')
    return '{0}\n    {1}'.format(
        category_line,
        comma.join(attribute_color.wrap_text(attr.name) for attr in attrs),
    )


def _format_multiline_with_doc(category, attrs):
    category_line = category_color.wrap_text(str(category) + ':') + '\n'
    return category_line + '\n'.join(
        '    {0} {1}'.format(
            attribute_color.wrap_text(attr.name + ':'), doc_color.wrap_text(attr.doc)
        )
        for attr in attrs
    )


def _format_descriptor(category, attrs):
    return _format_multiline_with_doc(category, attrs)


_AttributeGroupFormatter = namedtuple(
    '_AttributeGroupFormatter', ['display_index', 'formatter']
)

_single_line = _AttributeGroupFormatter(display_index=0, formatter=_format_single_line)
_descriptor = _AttributeGroupFormatter(display_index=1, formatter=_format_descriptor)
_multiline_with_doc = _AttributeGroupFormatter(
    display_index=2, formatter=_format_multiline_with_doc
)

_FORMATTER = {
    AttrCategory.FUNCTION: _multiline_with_doc,
    AttrCategory.CLASS: _multiline_with_doc,
    AttrCategory.EXCEPTION: _multiline_with_doc,
    AttrCategory.PROPERTY: _single_line,
    # Attribute
    AttrCategory.MODULE_ATTRIBUTE: _single_line,
    AttrCategory.SPECIAL_ATTRIBUTE: _single_line,
    # Function
    AttrCategory.MAGIC: _multiline_with_doc,
    AttrCategory.ARITHMETIC: _single_line,
    AttrCategory.ITER: _single_line,
    AttrCategory.CONTEXT_MANAGER: _single_line,
    AttrCategory.OBJECT_CUSTOMIZATION: _single_line,
    AttrCategory.RICH_COMPARISON: _single_line,
    AttrCategory.ATTRIBUTE_ACCESS: _single_line,
    AttrCategory.DESCRIPTOR: _descriptor,
    AttrCategory.DESCRIPTOR_CLASS: _single_line,
    AttrCategory.STATIC_METHOD: _descriptor,
    AttrCategory.CLASS_CUSTOMIZATION: _single_line,
    AttrCategory.CONTAINER: _single_line,
    AttrCategory.COUROUTINE: _single_line,
    AttrCategory.COPY: _single_line,
    AttrCategory.PICKLE: _single_line,
    AttrCategory.ABSTRACT_CLASS: _single_line,
}
