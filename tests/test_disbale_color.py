def test_color_disabled():
    from pdir.color import _ColorDisabled

    c = _ColorDisabled()
    assert c.wrap_text("foobar") == "foobar"

    d = _ColorDisabled()
    assert c == d
    assert c is not d
