import pytest
from tdoptions import td

# https://docs.pytest.org/en/6.2.x/getting-started.html
# https://docs.pytest.org/en/6.2.x/monkeypatch.html
# https://docs.pytest.org/en/6.2.x/fixture.html
# https://docs.pytest.org/en/6.2.x/capture.html

@pytest.fixture
def client(monkeypatch):
    c = td.Td()
    return c

class TestTd:
    #class MockGet:
    #    text = 'This test sucks'

    #    @staticmethod
    #    def get(*args):
    #        return 'asdf'
    #
    #def test_open_url(self, monkeypatch, url):
    #    def mock_get(*args, **kwargs):
    #        return self.MockGet()

    #    monkeypatch.setattr(module.requests, 'get', mock_get)
    #    assert url.open_url() == 'This test sucks'

    def test_options(self):
        assert False

    def test_underlying(self):
        assert False

