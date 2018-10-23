"""
Test user configuration.

The file name 'test_zz_config' is intended for making pytest run this file
last, because in Python 2, for unknown reasons, if del modules[module] in
clean() is executed before executing other tests, those tests will fail.
Since pytest discover test files in alphabetic order, inserting a 'z_' puts
it last.
"""

import os
import shutil
from sys import modules

import pytest
from pdir.color import COLORS

if pytest.__version__[0] == '2':
    from pytest import yield_fixture as fixture
elif pytest.__version__[0] == '3':
    from pytest import fixture as fixture


@fixture
def clean():
    DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.pdir2config')
    yield DEFAULT_CONFIG_FILE
    if 'PDIR2_CONFIG_FILE' in os.environ:
        if os.path.exists(os.environ['PDIR2_CONFIG_FILE']):
            os.remove(os.environ['PDIR2_CONFIG_FILE'])
        del os.environ['PDIR2_CONFIG_FILE']
    if os.path.exists(DEFAULT_CONFIG_FILE):
        os.remove(DEFAULT_CONFIG_FILE)
    for module in (
        'pdir',
        'pdir.api',
        'pdir.constants',
        'pdir.format',
        'pdir.configuration',
        'pdir.color',
        'pdir.utils',
    ):
        try:
            del modules[module]
        except KeyError:
            pass


def test_default_env_without_config(clean):
    import pdir

    pdir()


def test_set_env_without_config(clean):
    os.environ['PDIR2_CONFIG_FILE'] = 'aaa'
    with pytest.raises(OSError, message='Config file not exist: aaa'):
        import pdir

        pdir()


def test_read_config(clean):
    # 'clean' is the DEFAULT_CONFIG_FILE yielded from fixture.
    shutil.copyfile('tests/data/config_1.ini', clean)
    from pdir.format import doc_color, category_color, attribute_color, comma

    assert doc_color == COLORS['white']
    assert category_color == COLORS['bright yellow']
    assert comma == '\033[1;32m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_read_config_from_custom_location(clean):
    os.environ['PDIR2_CONFIG_FILE'] = os.path.join(os.path.expanduser('~'), '.myconfig')
    shutil.copyfile('tests/data/config_1.ini', os.environ['PDIR2_CONFIG_FILE'])
    from pdir.format import doc_color, category_color, attribute_color, comma

    assert doc_color == COLORS['white']
    assert category_color == COLORS['bright yellow']
    assert comma == '\033[1;32m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_uniform_color(clean):
    shutil.copyfile('tests/data/config_2.ini', clean)
    from pdir.format import doc_color, category_color, attribute_color, comma

    assert doc_color == COLORS['white']
    assert category_color == COLORS['white']
    assert comma == '\033[0;37m, \033[0m'
    assert attribute_color == COLORS['white']


def test_empty_config(clean):
    shutil.copyfile('tests/data/empty_config.ini', clean)
    from pdir.format import doc_color, category_color, attribute_color, comma

    assert doc_color == COLORS['grey']
    assert category_color == COLORS['yellow']
    assert comma == '\033[1;30m, \033[0m'
    assert attribute_color == COLORS['cyan']


def test_invalid_config_1(clean):
    shutil.copyfile('tests/data/error_config_1.ini', clean)
    with pytest.raises(ValueError, message='Invalid key: doc-color1'):
        import pdir

        pdir()


def test_invalid_config_2(clean):
    shutil.copyfile('tests/data/error_config_2.ini', clean)
    with pytest.raises(ValueError, message='Invalid color value: 42'):
        import pdir

        pdir()
