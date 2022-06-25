import pytest
from unittest.mock import patch

@pytest.fixture(scope="session")
def tty():
    with patch("sys.stdout.isatty") as faketty:
        faketty.return_value = True
        yield
