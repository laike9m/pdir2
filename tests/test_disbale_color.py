from pdir.color import _ColorDisabled


def test_color_disabled():
    c = _ColorDisabled()
    assert c.wrap_text("foobar") == "foobar"

    d = _ColorDisabled()
    assert c == d
    assert c is not d
