"""Configuration management setup
"""

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os

from .constants import *
from .color import COLOR_TABLE


class Configuration(object):

    DEFAULT_CONFIG = {
        UNIFORM_COLOR: None,
        CATEGORY_COLOR: YELLOW,
        ATTRIBUTE_COLOR: CYAN,
        COMMA_COLOR: GREY,
        DOC_COLOR: GREY,
    }

    def __init__(self):
        self._configparser = ConfigParser()
        self._config = self.DEFAULT_CONFIG
        self._load()

    @property
    def uniform_color(self):
        return COLOR_TABLE.get(self._config[UNIFORM_COLOR], None)

    @property
    def category_color(self):
        return COLOR_TABLE[self._config[CATEGORY_COLOR]]

    @property
    def attribute_color(self):
        return COLOR_TABLE[self._config[ATTRIBUTE_COLOR]]

    @property
    def comma_color(self):
        return COLOR_TABLE[self._config[COMMA_COLOR]]

    @property
    def doc_color(self):
        return COLOR_TABLE[self._config[DOC_COLOR]]

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
            uniform_color = user_config_dict[UNIFORM_COLOR]
            for key in self._config:
                self._config[key] = uniform_color
            return

        for key, value in user_config_dict.items():
            if key not in VALID_CONFIG_KEYS:
                raise ValueError('Invalid key: %s' % key)
            if value not in VALID_COLORS:
                raise ValueError('Invalid color value: %s' % value)
            self._config[key] = value


cfg = Configuration()
