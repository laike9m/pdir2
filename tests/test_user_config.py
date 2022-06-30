"""
Test user configuration.
"""

import os
import shutil

import pytest


def test_default_env_without_config(fake_tty, clean_cached_modules):
    import pdir

    pdir()


def test_set_env_without_config(fake_tty, clean_cached_modules):
    os.environ['PDIR2_CONFIG_FILE'] = 'aaa'
    with pytest.raises(OSError, match='Config file not exist: aaa'):
        import pdir

        pdir()


def test_read_config(fake_tty, clean_cached_modules):
    # 'clean' is the DEFAULT_CONFIG_FILE yielded from fixture.
    shutil.copyfile('tests/data/config_1.ini', clean_cached_modules)
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLORS

    assert doc_color == COLORS['white']
    assert category_color == COLORS['bright yellow']
    assert comma == '\033[1;32m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_config_disable_color_tty(fake_tty, clean_cached_modules):
    # 'clean' is the DEFAULT_CONFIG_FILE yielded from fixture.
    shutil.copyfile('tests/data/config_disable_color.ini', clean_cached_modules)
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLOR_DISABLED

    assert doc_color == COLOR_DISABLED
    assert category_color == COLOR_DISABLED
    assert comma == ', '
    assert attribute_color == COLOR_DISABLED


def test_config_auto_color_tty(fake_tty, clean_cached_modules):
    # 'clean' is the DEFAULT_CONFIG_FILE yielded from fixture.
    shutil.copyfile('tests/data/config_auto_color.ini', clean_cached_modules)
    from pdir.format import doc_color
    from pdir.color import COLORS

    assert doc_color == COLORS['grey']


def test_config_enable_color_not_tty(clean_cached_modules):
    # 'clean' is the DEFAULT_CONFIG_FILE yielded from fixture.
    shutil.copyfile('tests/data/config_enable_color.ini', clean_cached_modules)
    from pdir.format import doc_color
    from pdir.color import COLORS

    assert doc_color == COLORS['grey']


def test_env_disable_color_even_config_set(fake_tty, clean_cached_modules):
    shutil.copyfile('tests/data/config_enable_color.ini', clean_cached_modules)
    os.environ['PDIR2_NOCOLOR'] = "true"
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLOR_DISABLED

    assert doc_color == COLOR_DISABLED
    assert category_color == COLOR_DISABLED
    assert comma == ', '
    assert attribute_color == COLOR_DISABLED

    del os.environ['PDIR2_NOCOLOR']


def test_read_config_from_custom_location(fake_tty, clean_cached_modules):
    os.environ['PDIR2_CONFIG_FILE'] = os.path.join(os.path.expanduser('~'), '.myconfig')
    shutil.copyfile('tests/data/config_1.ini', os.environ['PDIR2_CONFIG_FILE'])
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLORS

    assert doc_color == COLORS['white']
    assert category_color == COLORS['bright yellow']
    assert comma == '\033[1;32m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_uniform_color(fake_tty, clean_cached_modules):
    shutil.copyfile('tests/data/config_2.ini', clean_cached_modules)
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLORS

    assert doc_color == COLORS['white']
    assert category_color == COLORS['white']
    assert comma == '\033[0;37m, \033[0m'
    assert attribute_color == COLORS['white']


def test_empty_config(fake_tty, clean_cached_modules):
    shutil.copyfile('tests/data/empty_config.ini', clean_cached_modules)
    from pdir.format import doc_color, category_color, attribute_color, comma
    from pdir.color import COLORS

    assert doc_color == COLORS['grey']
    assert category_color == COLORS['yellow']
    assert comma == '\033[1;30m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_invalid_config_1(clean_cached_modules):
    shutil.copyfile('tests/data/error_config_1.ini', clean_cached_modules)
    with pytest.raises(ValueError, match='Invalid key: doc-color1'):
        import pdir

        pdir()


def test_invalid_config_2(clean_cached_modules):
    shutil.copyfile('tests/data/error_config_2.ini', clean_cached_modules)
    with pytest.raises(ValueError, match='Invalid color value: 42'):
        import pdir

        pdir()
