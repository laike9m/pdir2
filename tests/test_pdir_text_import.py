import sys

import pdir


def test_pdir_text():
    result = pdir('hlm')
    if sys.version[0] == '2':
        assert repr(result) == '\n'.join([
            '\x1b[0;33mmodule attribute:\x1b[0;m',(
                '    \x1b[0;36m__file__\x1b[0;m\x1b[1;30m,'
                ' \x1b[0;m\x1b[0;36m__name__\x1b[0;m\x1b[1;30m,'
                ' \x1b[0;m\x1b[0;36m__package__\x1b[0;m'),
            '\x1b[0;33mother:\x1b[0;m',
            '    \x1b[0;36m__builtins__\x1b[0;m',
            '\x1b[0;33mspecial attribute:\x1b[0;m',
            '    \x1b[0;36m__doc__\x1b[0;m',
            '\x1b[0;33mclass:\x1b[0;m',
            '    \x1b[0;36mChild:\x1b[0;m \x1b[1;30m\x1b[0;m',
            '    \x1b[0;36mMaster:\x1b[0;m \x1b[1;30mOOO today.\x1b[0;m'

        ])
    else:
        assert repr(result) == '\n'.join([
            '\x1b[0;33mmodule attribute:\x1b[0;m',(
                '    \x1b[0;36m__file__\x1b[0;m\x1b[1;30m,'
                ' \x1b[0;m\x1b[0;36m__package__\x1b[0;m'),
            '\x1b[0;33mother:\x1b[0;m',
            '    \x1b[0;36m__builtins__\x1b[0;m',
            '\x1b[0;33mspecial attribute:\x1b[0;m',(
                '    \x1b[0;36m__doc__\x1b[0;m\x1b[1;30m,'
                ' \x1b[0;m\x1b[0;36m__name__\x1b[0;m'),
            '\x1b[0;33mclass:\x1b[0;m',
            '    \x1b[0;36mChild:\x1b[0;m \x1b[1;30m\x1b[0;m',
            '    \x1b[0;36mMaster:\x1b[0;m \x1b[1;30mOOO today.\x1b[0;m'
        ])
    print(result)

def test_sub_import_and_search():
    result = pdir('hlm.Master.child').s('hlm')
    expected = '\x1b[0;33mother:\x1b[0;m\n    \x1b[0;36mhlm\x1b[0;m'
    assert repr(result) == expected, "Expected {!r}, got {!r}".format(expected, result)

