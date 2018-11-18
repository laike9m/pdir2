import pdir


def test_search_without_argument():
    foo = 1
    bar = 1
    baz = 1
    apple1 = 1
    xapple2 = 1
    result, result2 = pdir().s('apple'), pdir().search('apple')
    assert repr(result) == (
        '\x1b[0;33mproperty:\x1b[0m\n'
        '    \x1b[0;36mapple1\x1b[0m\x1b[1;30m,'
        ' \x1b[0m\x1b[0;36mxapple2\x1b[0m'
    )
    assert repr(result2) == (
        '\x1b[0;33mproperty:\x1b[0m\n'
        '    \x1b[0;36mapple1\x1b[0m\x1b[1;30m,'
        ' \x1b[0m\x1b[0;36mxapple2\x1b[0m'
    )


def test_search_with_argument():
    class T:
        pass

    result, result2 = pdir(T).s('attr'), pdir(T).search('attr')
    result3, result4 = pdir(T).s('Attr'), pdir(T).search('Attr')
    expected = '\n'.join(
        [
            '\x1b[0;33mattribute access:\x1b[0m',
            (
                '    \x1b[0;36m__delattr__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__getattribute__\x1b[0m\x1b[1;30m, '
                '\x1b[0m\x1b[0;36m__setattr__\x1b[0m'
            ),
        ]
    )
    assert repr(result) == expected
    assert repr(result2) == expected
    assert repr(result3) == expected
    assert repr(result4) == expected

    # Case sensitive
    result5, result6 = pdir(T).s('Attr', True), pdir(T).search('Attr', True)
    assert repr(result5) == ''
    assert repr(result6) == ''
