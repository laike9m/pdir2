"""Configuration management setup
"""

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os
from os.path import expanduser

from .color import COLORS

# User Configuration
DEFAULT_CONFIG_FILE = expanduser('~/.pdir2config')
CONFIG_FILE_ENV = 'PDIR2_CONFIG_FILE'
DEFAULT = 'global'
UNIFORM_COLOR = 'uniform-color'
CATEGORY_COLOR = 'category-color'
ATTRIBUTE_COLOR = 'attribute-color'
COMMA_COLOR = 'comma-color'
DOC_COLOR = 'doc-color'
VALID_CONFIG_KEYS = frozenset(
    {UNIFORM_COLOR, CATEGORY_COLOR, ATTRIBUTE_COLOR, COMMA_COLOR, DOC_COLOR}
)


class Configuration(object):

    _uniform_color = None
    _category_color = COLORS['yellow']
    _attribute_color = COLORS['cyan']
    _comma_color = COLORS['grey']
    _doc_color = COLORS['grey']

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

    def _load(self):
        config_file = os.environ.get(CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE)
        config_file = os.path.expanduser(config_file)
        if not os.path.exists(config_file):
            if config_file == DEFAULT_CONFIG_FILE:
                # Only raise exception if user set CONFIG_FILE_ENV.
                return
            else:
                raise OSError('Config file not exist: %s' % config_file)

        self._configparser.read(config_file)
        if not self._configparser.has_section(DEFAULT):
            return
        user_config_dict = dict(self._configparser.items(DEFAULT))

        # UNIFORM_COLOR suppresses other settings.
        if UNIFORM_COLOR in user_config_dict:
            self._uniform_color = COLORS[user_config_dict[UNIFORM_COLOR]]
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
else:
    category_color = _cfg.category_color
    attribute_color = _cfg.attribute_color
    doc_color = _cfg.doc_color
    comma = _cfg.comma_color.wrap_text(', ')
