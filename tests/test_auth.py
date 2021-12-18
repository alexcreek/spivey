from datetime import datetime as dt
from datetime import timezone, timedelta
import pytest
import requests
from spivey.auth import Auth

class MockResponse:
    status_code = 200

    @staticmethod
    def json():
        return {'access_token': 'asdf',
                'expires_in': 999}

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

    def test_token_as_a_header(self, mock_token):
        a = Auth()
        assert a.header() == {'Authorization': 'Bearer asdf'}

    def test_token_as_a_string(self, mock_token):
        a = Auth()
        assert a.token() == 'asdf'

    def test_ttl_being_valid(self, monkeypatch, mock_token):
        a = Auth()
        monkeypatch.setattr(a, 'ttl', dt.now(timezone.utc) + timedelta(minutes=10))
        monkeypatch.setattr(a, '_token', 'aaa')
        assert a.token() == 'aaa'

    def test_ttl_being_expired(self, monkeypatch, mock_token):
        a = Auth()
        monkeypatch.setattr(a, 'ttl', dt.now(timezone.utc) - timedelta(minutes=10))
        assert a.token() == 'asdf'
