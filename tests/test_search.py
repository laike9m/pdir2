import pdir


def test_search_without_argument():
    dadada = 1
    cadada = 1
    vadada = 1
    apple1 = 1
    xapple2 = 1
    assert repr(pdir().s('apple')) == (
        '\x1b[0;33mother:\x1b[0;m\n'
        '    \x1b[0;36mapple1\x1b[0;m\x1b[1;30m,'
        ' \x1b[0;m\x1b[0;36mxapple2\x1b[0;m')
    assert repr(pdir().search('apple')) == (
        '\x1b[0;33mother:\x1b[0;m\n'
        '    \x1b[0;36mapple1\x1b[0;m\x1b[1;30m,'
        ' \x1b[0;m\x1b[0;36mxapple2\x1b[0;m')


def test_search_with_argument():
    class T(object):
        pass
    assert repr(pdir(T).s('attr')) == '\n'.join([
        '\x1b[0;33mattribute access:\x1b[0;m', (
            '    \x1b[0;36m__delattr__\x1b[0;m\x1b[1;30m, '
            '\x1b[0;m\x1b[0;36m__getattribute__\x1b[0;m\x1b[1;30m, '
            '\x1b[0;m\x1b[0;36m__setattr__\x1b[0;m')])
    assert repr(pdir(T).search('attr')) == '\n'.join([
        '\x1b[0;33mattribute access:\x1b[0;m', (
            '    \x1b[0;36m__delattr__\x1b[0;m\x1b[1;30m, '
            '\x1b[0;m\x1b[0;36m__getattribute__\x1b[0;m\x1b[1;30m, '
            '\x1b[0;m\x1b[0;36m__setattr__\x1b[0;m')])
