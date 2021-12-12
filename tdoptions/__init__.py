import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from json import JSONDecodeError
from .auth import Auth
from . import http

class Client():
    """
    Client for interacting with the tdameritrade api
    """
    def __init__(self):
        self.auth = Auth()
        self.url = os.getenv('TD_URL', 'https://api.tdameritrade.com/v1/marketdata')
        self.timeout  = int(os.getenv('TD_TIMEOUT', '30'))

    def options(self, ticker, days):
        """
        Fetch an option chain

        :param ticker: Ticker of the underlying asset
        :param days: Get all contracts whose expiration <= this
        :return: nested data structure of options chains
        :rtype: dict
        """

        today = dt.today()
        # timedelta is for adding And subtracting time, not just a delta
        to_date = today + timedelta(int(days))
        tfmt = '%Y-%m-%d'

        headers = self.auth.header()
        payload = {
            'symbol': ticker.upper(),
            'fromDate': today.strftime(tfmt),
            'toDate': to_date.strftime(tfmt)
        }

        r = http.get(f'{self.url}/chains', headers=headers, params=payload,
            timeout=self.timeout
        )

        try:
            output = r.json()
        except JSONDecodeError:
            print(f'Caught JSONDecodeError: response contained invalid json - {r.text}')
            sys.exit(1)
        return output


    def underlying(self, ticker):
        """
        Fetch the price for an option's underlying asset

        :param ticker: Ticker of the asset
        :return: lastPrice of the asset
        :rtype: dict
        """

        ticker = ticker.upper()
        headers = self.auth.header()
        r = http.get(f'{self.url}/{ticker}/quotes', headers=headers, timeout=self.timeout)

        try:
            output = r.json()
        except JSONDecodeError:
            print(f'Caught JSONDecodeError: response contained invalid json - {r.text}')
            sys.exit(1)

        if ticker in output.keys():
            return float(output[ticker]['lastPrice'])
        print(f'No data found for {ticker}')
        return float(-1.0)
