"""Configuration management setup
"""

import os
from configparser import ConfigParser
from os.path import expanduser

from .color import COLORS

# User Configuration
_DEFAULT_CONFIG_FILE = expanduser('~/.pdir2config')
_DEFAULT = 'global'
_UNIFORM_COLOR = 'uniform-color'
VALID_CONFIG_KEYS = frozenset(
    {
        _UNIFORM_COLOR,
        'category-color',
        'attribute-color',
        'comma-color',
        'doc-color',
        'slot-color',
    }
)


class Configuration:

    _uniform_color = None
    _category_color = COLORS['yellow']
    _attribute_color = COLORS['cyan']
    _comma_color = COLORS['grey']
    _doc_color = COLORS['grey']
    _slot_color = COLORS['magenta']

    def __init__(self):
        self._configparser = ConfigParser()
        self._load()

    @property
    def uniform_color(self):
        return self._uniform_color

    @property
    def category_color(self):
        return self._category_color

    @property
    def attribute_color(self):
        return self._attribute_color

    @property
    def comma_color(self):
        return self._comma_color

    @property
    def doc_color(self):
        return self._doc_color

    @property
    def slot_color(self):
        return self._slot_color

    def _load(self):
        config_file = os.environ.get('PDIR2_CONFIG_FILE', _DEFAULT_CONFIG_FILE)
        config_file = os.path.expanduser(config_file)
        if not os.path.exists(config_file):
            if config_file == _DEFAULT_CONFIG_FILE:
                # Only raise exception if user set CONFIG_FILE_ENV.
                return
            else:
                raise OSError('Config file not exist: %s' % config_file)

        self._configparser.read(config_file)
        if not self._configparser.has_section(_DEFAULT):
            return
        user_config_dict = dict(self._configparser.items(_DEFAULT))

        # UNIFORM_COLOR suppresses other settings.
        if _UNIFORM_COLOR in user_config_dict:
            self._uniform_color = COLORS[user_config_dict[_UNIFORM_COLOR]]
            return

        for item, color in user_config_dict.items():
            if item not in VALID_CONFIG_KEYS:
                raise ValueError('Invalid key: %s' % item)
            if color not in set(COLORS.keys()):
                raise ValueError('Invalid color value: %s' % color)
            # item uses "-", e.g. "doc-color"
            self.__setattr__('_' + item.replace('-', '_'), COLORS[color])


_cfg = Configuration()

if _cfg.uniform_color:
    category_color = attribute_color = doc_color = _cfg.uniform_color
    comma = _cfg.uniform_color.wrap_text(', ')
    slot_tag = _cfg.uniform_color.wrap_text('(slotted)')
else:
    category_color = _cfg.category_color
    attribute_color = _cfg.attribute_color
    doc_color = _cfg.doc_color
    comma = _cfg.comma_color.wrap_text(', ')
    slot_tag = _cfg.slot_color.wrap_text('(slotted)')
