from datetime import datetime as dt
import pytest
import requests
import tdoptions.auth
from tdoptions import Client

### Fixtures
class MockResponse():
    status_code = 200

    def __init__(self, *args, **kwargs):
        self.params = kwargs['params']

    def json(self):
        return self.params


class MockUnderlyingResponse():
    status_code = 200

    @staticmethod
    def json():
        return {'SPY': {'lastPrice': '123.0'}}


@pytest.fixture
def echo_get_params(monkeypatch):
    """
    Monkeypatches requests.get and returns any params sent with the request
    """
    def mock_get(*args, **kwargs):
        return MockResponse(*args, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def disable_auth(monkeypatch):
    """
    Monkeypatches the auth library and sets the needed env vars
    """
    def mock_token(*args, **kwargs):
        return 'asdf'

    monkeypatch.setattr(tdoptions.auth.Auth, "token", mock_token)
    monkeypatch.setenv('CLIENT_ID', 'asdf')
    monkeypatch.setenv('REFRESH_TOKEN', 'asdf')


### Tests
class TestOptions:
    def test_invalid_json(self, disable_auth, httpbin, monkeypatch):
        monkeypatch.setenv('TD_URL', f'{httpbin.url}/html')
        c = Client()
        with pytest.raises(SystemExit):
            c.options('spy', 7)

    def test_ticker_getting_uppercased(self, disable_auth, echo_get_params):
        c = Client()
        resp = c.options('spy', 7)
        assert resp['symbol'] == 'SPY'

    def test_date_formatting(self, disable_auth, echo_get_params):
        c = Client()
        resp = c.options('spy', 7)
        assert dt.strptime(resp['fromDate'], '%Y-%m-%d')
        assert dt.strptime(resp['toDate'], '%Y-%m-%d')

    def test_from_and_to_dates_equals_days_arg(self, disable_auth, echo_get_params):
        c = Client()
        resp = c.options('spy', 7)
        _from = dt.strptime(resp['fromDate'], '%Y-%m-%d')
        _to = dt.strptime(resp['toDate'], '%Y-%m-%d')
        assert _to.day - _from.day == 7

    def test_success(self, disable_auth, echo_get_params):
        c = Client()
        assert isinstance(c.options('spy', 7), dict)


class TestUnderlying:
    def test_invalid_json(self, disable_auth, httpbin, monkeypatch):
        monkeypatch.setenv('TD_URL', f'{httpbin.url}/html')
        c = Client()
        with pytest.raises(SystemExit):
            c.underlying('spy')

    def test_success(self, disable_auth, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockUnderlyingResponse()

        monkeypatch.setattr(requests, 'get', mock_get)
        c = Client()
        assert c.underlying('spy') == 123.0
