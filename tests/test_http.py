from contextlib import suppress
import pytest
import pytest_httpbin
from tdoptions import http

class TestGet:
    def test_timing_out(self, httpbin):
        with pytest.raises(SystemExit):
            http.get(f'{httpbin.url}/delay/2', timeout=1)

    def test_getting_rate_limited(self, httpbin):
        with pytest.raises(SystemExit):
            http.get(f'{httpbin.url}/status/429')

    @pytest.mark.parametrize('status', ['404', '502'])
    def test_4xx_and_5xx_responses(self, httpbin, status):
        with pytest.raises(SystemExit):
            http.get(f'{httpbin.url}/status/{status}')

    def test_retries(self, httpbin, capsys):
        with suppress(SystemExit):
            http.get(f'{httpbin.url}/status/504')
        assert capsys.readouterr().out.count('GATEWAY TIMEOUT') == 3


class TestPost:
    def test_timing_out(self, httpbin):
        with pytest.raises(SystemExit):
            http.post(f'{httpbin.url}/delay/2', timeout=1)

    def test_getting_rate_limited(self, httpbin):
        with pytest.raises(SystemExit):
            http.post(f'{httpbin.url}/status/429')

    @pytest.mark.parametrize('status', ['404', '502'])
    def test_4xx_and_5xx_responses(self, httpbin, status):
        with pytest.raises(SystemExit):
            http.post(f'{httpbin.url}/status/{status}')

    def test_retries(self, httpbin, capsys):
        with suppress(SystemExit):
            http.post(f'{httpbin.url}/status/504')
        assert capsys.readouterr().out.count('GATEWAY TIMEOUT') == 3
