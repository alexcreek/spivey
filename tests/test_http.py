from contextlib import suppress
import pytest
import requests
from tdoptions import http

@pytest.fixture
def mock_200():
    r = requests.models.Response()
    r.status_code = 200
    return r

@pytest.fixture
def mock_504():
    r = requests.models.Response()
    r.status_code = 504
    return r

class TestGet:
    def test_timing_out(self):
        with pytest.raises(SystemExit):
            http.get('http://10.255.255.1', timeout=1)

    def test_getting_rate_limited(self, httpbin):
        with pytest.raises(SystemExit):
            http.get(f'{httpbin.url}/status/429')

    @pytest.mark.parametrize('status', ['502', '504'])
    def test_5xx_responses(self, httpbin, status):
        with pytest.raises(SystemExit):
            http.get(f'{httpbin.url}/status/{status}')

    def test_retries(self, httpbin, capsys):
        with suppress(SystemExit):
            http.get(f'{httpbin.url}/status/504')
        assert capsys.readouterr().out.count('504 Error') == 3

    def test_successful_request(self, httpbin, capsys):
        print(http.get(f'{httpbin.url}/status/200'))
        assert capsys.readouterr().out.count('<Response [200]>') == 1

class TestPost:
    def test_timing_out(self):
        with pytest.raises(SystemExit):
            http.post('http://10.255.255.1', timeout=1)

    def test_getting_rate_limited(self, httpbin):
        with pytest.raises(SystemExit):
            http.post(f'{httpbin.url}/status/429')

    @pytest.mark.parametrize('status', ['502', '504'])
    def test_5xx_responses(self, httpbin, status):
        with pytest.raises(SystemExit):
            http.post(f'{httpbin.url}/status/{status}')

    def test_retries(self, httpbin, capsys):
        with suppress(SystemExit):
            http.post(f'{httpbin.url}/status/504')
        assert capsys.readouterr().out.count('504 Error') == 3

    def test_successful_request(self, httpbin, capsys):
        print(http.post(f'{httpbin.url}/status/200'))
        assert capsys.readouterr().out.count('<Response [200]>') == 1

class TestIsOk:
    def test_good_status_code(self, mock_200):
        assert http.is_ok(mock_200)

    def test_bad_status_code(self, mock_504):
        with pytest.raises(requests.exceptions.HTTPError):
            http.is_ok(mock_504)
