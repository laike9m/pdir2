from ._internal_utils import is_bpython


class Color(object):
    def __init__(self, color_code, bright=False):
        self.color_code = str(color_code)
        self.intensity = '1' if bright else '0'

    def wrap_text(self, text):
        if is_bpython():
            colored_text = '\033[%sm%s\033[0m' % (self.color_code, text)
            if self.intensity == '0':
                return colored_text
            else:
                return '\033[1m' + colored_text
        else:
            return '\033[%s;%sm%s\033[0m' % (self.intensity, self.color_code, text)

    def __eq__(self, other):
        return self.color_code == other.color_code

    def __repr__(self):
        return '\033[%sm%s\033[0m' % (self.color_code, 'color')


COLORS = {
    'black': Color(30),
    'bright black': Color(30, True),
    'grey': Color(30, True),
    'red': Color(31),
    'bright red': Color(31, True),
    'green': Color(32),
    'bright green': Color(32, True),
    'yellow': Color(33),
    'bright yellow': Color(33, True),
    'blue': Color(34),
    'bright blue': Color(34, True),
    'magenta': Color(35),
    'bright magenta': Color(35, True),
    'cyan': Color(36),
    'bright cyan': Color(36, True),
    'white': Color(37),
    'bright white': Color(37, True),
}
