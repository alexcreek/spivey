import pytest
import requests
from tdoptions.auth import Auth

class MockResponse:
    status_code = 200

    @staticmethod
    def json():
        return {'access_token': 'asdf'}

@pytest.fixture
def mock_token(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    monkeypatch.setenv('CLIENT_ID', 'asdf')
    monkeypatch.setenv('REFRESH_TOKEN', 'asdf')


class TestAuth:
    def test_missing_refresh_token(self, monkeypatch):
        monkeypatch.setenv('CLIENT_ID', 'asdf')
        with pytest.raises(SystemExit):
            a = Auth()
            a.header()

    def test_missing_client_id(self, monkeypatch):
        monkeypatch.setenv('REFRESH_TOKEN', 'asdf')
        with pytest.raises(SystemExit):
            a = Auth()
            a.header()

    def test_token_missing_from_response(self, monkeypatch, httpbin):
        monkeypatch.setenv('TD_AUTH_URL', f'{httpbin.url}/status/200')
        with pytest.raises(SystemExit):
            a = Auth()
            a.header()

    def test_token_as_a_header(self, monkeypatch, mock_token):
        a = Auth()
        assert a.header() == {'Authorization': 'Bearer asdf'}

    def test_token_as_a_string(self, monkeypatch, mock_token):
        a = Auth()
        assert a.token() == 'asdf'
