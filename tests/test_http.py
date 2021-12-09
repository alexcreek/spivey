import pytest
from tdoptions import auth

# https://docs.pytest.org/en/6.2.x/getting-started.html
# https://docs.pytest.org/en/6.2.x/monkeypatch.html
# https://docs.pytest.org/en/6.2.x/fixture.html
# https://docs.pytest.org/en/6.2.x/capture.html

class TestGet:
    def test_timing_out(self):
        assert False

    def test_getting_rate_limited(self):
        assert False


class TestPost:
    def test_timing_out(self):
        assert False

    def test_getting_rate_limited(self):
        assert False