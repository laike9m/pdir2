import os
import pytest
from unittest.mock import patch
from sys import modules

PDIR2_CONFIG_FILE = "PDIR2_CONFIG_FILE"


def remove_module_cache():
    """
    There are some global settings which are initialized when pdir firstly
    import, then after that, no matter how you change the config or mock
    ``isatty()`` functions, those global values (settings, mostly), will
    not change.

    So in order to make some of our patches or test configurations work, we
    need to clear the import cache. So that when we ``import pdir`` in test
    cases, those global values will be initialized again due to the lack of
    cache.

    more detail: https://www.kawabangga.com/posts/4706 (Chinese)
    """
    imported_modules = modules.keys()
    pdir_modules = [m for m in imported_modules if m.startswith('pdir')]
    for module in pdir_modules:
        try:
            del modules[module]
        except KeyError:
            pass


@pytest.fixture
def clean_cached_modules():
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
def fake_tty():
    with patch("sys.stdout.isatty") as faketty:
        faketty.return_value = True
        remove_module_cache()
        yield
