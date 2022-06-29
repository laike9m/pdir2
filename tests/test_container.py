def test_acting_like_a_list():
    import pdir

    dadada = 1
    cadada = 1
    vadada = 1
    apple1 = 1
    xapple2 = 1
    result, correct = pdir(), dir()
    assert len(correct) == len(result)

    for x, y in zip(correct, result):
        assert x == y


def test_acting_like_a_list_when_search():
    import pdir

    dadada = 1
    cadada = 1
    vadada = 1
    apple1 = 1
    xapple2 = 1
    result = pdir().s('apple')
    assert len(result) == 2
    assert list(result) == ['apple1', 'xapple2']


def test_attr_order():
    import pdir

    dir_attrs = dir(None)
    pdir_attrs = list(pdir(None))
    assert dir_attrs == pdir_attrs
