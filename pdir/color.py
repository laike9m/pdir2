from ._internal_utils import is_bpython
from typing_extensions import Protocol


class _Renderable(Protocol):
    def wrap_text(self, text: str) -> str:
        pass

    def __eq__(self, other: object) -> bool:
        pass


class _Color(_Renderable):
    def __init__(self, color_code: int, bright: bool = False) -> None:
        self.color_code = str(color_code)
        self.intensity = '1' if bright else '0'

    def wrap_text(self, text: str) -> str:
        if not is_bpython():
            return f'\033[{self.intensity};{self.color_code}m{text}\033[0m'

        colored_text = f'\033[{self.color_code}m{text}\033[0m'
        if self.intensity == '0':
            return colored_text
        else:
            return '\033[1m' + colored_text

    def __eq__(self, other: object) -> bool:  # type: ignore
        # __eq__ should work with any objects.
        # https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
        if not isinstance(other, _Color):
            return False

        return self.color_code == other.color_code

    def __repr__(self):
        return f'\033[{self.color_code}m{"color"}\033[0m'


class _ColorDisabled(_Renderable):
    def wrap_text(self, text: str) -> str:
        return text

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _ColorDisabled):
            return True
        return False


COLORS = {
    'black': _Color(30),
    'bright black': _Color(30, True),
    'grey': _Color(30, True),
    'red': _Color(31),
    'bright red': _Color(31, True),
    'green': _Color(32),
    'bright green': _Color(32, True),
    'yellow': _Color(33),
    'bright yellow': _Color(33, True),
    'blue': _Color(34),
    'bright blue': _Color(34, True),
    'magenta': _Color(35),
    'bright magenta': _Color(35, True),
    'cyan': _Color(36),
    'bright cyan': _Color(36, True),
    'white': _Color(37),
    'bright white': _Color(37, True),
}
COLOR_DISABLED = _ColorDisabled()
