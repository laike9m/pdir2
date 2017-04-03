from .constants import *


class Color(object):
    def __init__(self, name, color_code, bright=False):
        self.name = name
        self.color_code = color_code
        self.intensity = '1' if bright else '0'

    def __repr__(self):
        return ('', 'bright ')[self.intensity == '1'] + self.name

    def wrap_text(self, text):
        if repl_type == BPYTHON:
            colored_text = '\033[%sm%s\033[0m' % (self.color_code, text)
            if self.intensity == '0':
                return colored_text
            else:
                return '\033[1m' + colored_text
        else:
            return '\033[%s;%sm%s\033[0m' % (self.intensity, self.color_code,
                                             text)


COLOR_TABLE = {
    BLACK: Color(BLACK, '30'),
    BRIGHT_BLACK: Color(BRIGHT_BLACK, '30', True),
    GREY: Color(GREY, '30', True),
    RED: Color(RED, '31'),
    BRIGHT_RED: Color(BRIGHT_RED, '31', True),
    GREEN: Color(GREEN, '32'),
    BRIGHT_GREEN: Color(BRIGHT_GREEN, '32', True),
    YELLOW: Color(YELLOW, '33'),
    BRIGHT_YELLOW: Color(BRIGHT_YELLOW, '33', True),
    BLUE: Color(BLUE, '34'),
    BRIGHT_BLUE: Color(BRIGHT_BLUE, '34', True),
    MAGENTA: Color(MAGENTA, '35'),
    BRIGHT_MAGENTA: Color(BRIGHT_MAGENTA, '35', True),
    CYAN: Color(CYAN, '36'),
    BRIGHT_CYAN: Color(BRIGHT_CYAN, '36', True),
    WHITE: Color(WHITE, '37'),
    BRIGHT_WHITE: Color(BRIGHT_WHITE, '37', True),
}
