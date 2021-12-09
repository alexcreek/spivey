import pytest
from package import module

# https://docs.pytest.org/en/6.2.x/getting-started.html
# https://docs.pytest.org/en/6.2.x/monkeypatch.html
# https://docs.pytest.org/en/6.2.x/fixture.html
# https://docs.pytest.org/en/6.2.x/capture.html

@pytest.fixture
def url(monkeypatch):
    u = module.Url('aol.com')
    return u

class TestUrl:

    class MockGet:
        text = 'This test sucks'

        @staticmethod
        def get(*args):
            return 'asdf'

    def test_get_url(self, url):
        assert url.get_url() == 'aol.com'

    def test_set_url(self, url):
        url.set_url('asdf.com')
        assert getattr(url, 'url') == 'asdf.com'

    def test_open_url(self, monkeypatch, url):
        def mock_get(*args, **kwargs):
            return self.MockGet()

        monkeypatch.setattr(module.requests, 'get', mock_get)
        assert url.open_url() == 'This test sucks'
