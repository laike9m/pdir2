import sys
import pytest


def test_formatter_integrity(fake_tty):
    from pdir.attr_category import AttrCategory
    from pdir.format import _FORMATTER

    for ac in AttrCategory:
        assert ac in _FORMATTER


def test_pdir_module(fake_tty):
    import pdir
    import m

    result = pdir(m)
    expected = '\n'.join(
        [
            '\x1b[0;33mproperty:\x1b[0m',
            (
                '    \x1b[0;36m__builtins__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36ma\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36mb\x1b[0m'
            ),
            '\x1b[0;33mmodule attribute:\x1b[0m',
            (
                '    \x1b[0;36m__cached__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__file__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__loader__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__name__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__package__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__spec__\x1b[0m'
            ),
            '\x1b[0;33mspecial attribute:\x1b[0m',
            '    \x1b[0;36m__doc__\x1b[0m',
            '\x1b[0;33mclass:\x1b[0m',
            '    \x1b[0;36mOOO\x1b[0m\x1b[0;36m: '
            '\x1b[0m\x1b[1;30mOOO today.\x1b[0m',
            '\x1b[0;33mfunction:\x1b[0m',
            (
                '    \x1b[0;36mfunc\x1b[0m\x1b[0;36m: '
                '\x1b[0m\x1b[1;30mThis is a function\x1b[0m'
            ),
        ]
    )
    assert repr(result) == expected
    print(result)
    del m


def test_pdir_object(fake_tty):
    import pdir

    class T:
        def what(self):
            """doc line"""
            pass

    result = pdir(T())
    print(result)  # TODO: add real test.


def test_dir_without_argument(fake_tty):
    import pdir

    a = 1
    b = 2

    def whatever():
        """One line doc."""
        pass

    result = pdir()
    assert repr(result) == '\n'.join(
        [
            '\x1b[0;33mproperty:\x1b[0m',
            (
                '    \x1b[0;36ma\x1b[0m\x1b[1;30m, \x1b[0m\x1b[0;36mb\x1b[0m'
                '\x1b[1;30m, \x1b[0m\x1b[0;36mfake_tty\x1b[0m'
            ),
            '\x1b[0;33mclass:\x1b[0m',
            (
                '    \x1b[0;36mpdir\x1b[0m\x1b[0;36m: \x1b[0m\x1b[1;30mClass '
                'that provides pretty dir and search API.\x1b[0m'
            ),
            '\x1b[0;33mfunction:\x1b[0m',
            (
                '    \x1b[0;36mwhatever\x1b[0m\x1b[0;36m: '
                '\x1b[0m\x1b[1;30mOne line doc.\x1b[0m'
            ),
        ]
    )
    print(result)


def test_slots(fake_tty):
    import pdir

    class A:
        __slots__ = ['__mul__', '__hash__', 'a', 'b']

    a = A()
    result = pdir(a)

    expected = '\n'.join(
        [
            '\x1b[0;33mspecial attribute:\x1b[0m',
            (
                '    \x1b[0;36m__class__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__doc__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__module__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__slots__\x1b[0m'
            ),
            '\x1b[0;33mabstract class:\x1b[0m',
            '    \x1b[0;36m__subclasshook__\x1b[0m',
            '\x1b[0;33marithmetic:\x1b[0m',
            '    \x1b[0;36m__mul__\x1b[0m\x1b[0;35m(slotted)\x1b[0m',
            '\x1b[0;33mobject customization:\x1b[0m',
            (
                '    \x1b[0;36m__format__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__hash__\x1b[0m'
                '\x1b[0;35m(slotted)\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__init__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__new__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__repr__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__sizeof__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__str__\x1b[0m'
            ),
            '\x1b[0;33mrich comparison:\x1b[0m',
            (
                '    \x1b[0;36m__eq__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__ge__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__gt__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__le__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__lt__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__ne__\x1b[0m'
            ),
            '\x1b[0;33mattribute access:\x1b[0m',
            (
                '    \x1b[0;36m__delattr__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__dir__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__getattribute__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__setattr__\x1b[0m'
            ),
            '\x1b[0;33mclass customization:\x1b[0m',
            '    \x1b[0;36m__init_subclass__\x1b[0m',
            '\x1b[0;33mpickle:\x1b[0m',
            (
                (
                    '    \x1b[0;36m__getstate__\x1b[0m\x1b[1;30m, '
                    '\x1b[0m\x1b[0;36m__reduce__\x1b[0m\x1b[1;30m, '
                    '\x1b[0m\x1b[0;36m__reduce_ex__\x1b[0m'
                )
                if sys.version_info >= (3, 11)
                else (
                    '    \x1b[0;36m__reduce__\x1b[0m\x1b[1;30m, '
                    '\x1b[0m\x1b[0;36m__reduce_ex__\x1b[0m'
                )
            ),
            '\x1b[0;33mdescriptor:\x1b[0m',
            (
                '    \x1b[0;36ma\x1b[0m'
                '\x1b[0;35m(slotted)\x1b[0m\x1b[0;36m: '
                '\x1b[0m\x1b[1;30mclass member_descriptor with '
                'getter, setter, deleter\x1b[0m'
            ),
            (
                '    \x1b[0;36mb\x1b[0m'
                '\x1b[0;35m(slotted)\x1b[0m\x1b[0;36m: '
                '\x1b[0m\x1b[1;30mclass member_descriptor with '
                'getter, setter, deleter\x1b[0m'
            ),
        ]
    )
    assert repr(result) == expected


@pytest.mark.parametrize(
    'docstring, first_line',
    [
        ('', ''),
        ('Foobar', 'Foobar'),
        ('Foobar.', 'Foobar.'),
        ('Foo\nbar', 'Foo bar'),
        ('Foo\nbar.', 'Foo bar.'),
        ('Return nothing.\nNo exceptions.', 'Return nothing.'),
        ('Return a.b as\nresult', 'Return a.b as result'),
    ],
)
def test_get_first_line_of_docstring(docstring, first_line, fake_tty):
    from pdir._internal_utils import get_first_sentence_of_docstring

    CustomClass = type('CustomClass', (object,), {})
    setattr(CustomClass, '__doc__', docstring)
    assert get_first_sentence_of_docstring(CustomClass) == first_line
