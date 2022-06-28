import os
import pytest
from unittest.mock import patch
from sys import modules

PDIR2_CONFIG_FILE = "PDIR2_CONFIG_FILE"

def remove_module_cache():
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


@pytest.fixture
def clean():
    remove_module_cache()

    DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.pdir2config')
    yield DEFAULT_CONFIG_FILE
    if PDIR2_CONFIG_FILE in os.environ:
        if os.path.exists(os.environ[PDIR2_CONFIG_FILE]):
            os.remove(os.environ[PDIR2_CONFIG_FILE])
        del os.environ[PDIR2_CONFIG_FILE]
    if os.path.exists(DEFAULT_CONFIG_FILE):
        os.remove(DEFAULT_CONFIG_FILE)


@pytest.fixture(scope="session")
def enforce_tty_output():
    with patch("sys.stdout.isatty") as faketty:
        faketty.return_value = True
        remove_module_cache()
        yield
