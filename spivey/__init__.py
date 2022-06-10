import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from json import JSONDecodeError
from dateutil.parser import parse
from .auth import Auth
from . import http

class Client():
    """
    Client for interacting with the tdameritrade api
    """
    def __init__(self):
        self.auth = Auth()
        self.url = os.getenv('TD_URL', 'https://api.tdameritrade.com/v1/marketdata')
        self.timeout = int(os.getenv('TD_TIMEOUT', '30'))

        try:
            account_id = os.environ['TD_ACCOUNT_ID'] # Your account number without the trailing TDA
        except KeyError as e:
            print(f'{e} environment variable not found')
            sys.exit(1)

        self.order_url = f'https://api.tdameritrade.com/v1/accounts/{account_id}/orders'

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
        :rtype: float
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
        return None

    def buy_oco(self, capital, symbol, price, limit, stop):
        """
        Execute a One-Cancels-the-Other Buy order.

        :param capital: The amount of capital to use for the order.
        :param symbol: The contract's full symbol.
        :param price: The price to purchase the contract at.
        :param limit: The limit to sell at.
        :param stop: The stop to sell at.
        :rtype: bool
        """
        # Calculate how many options to buy
        quantity = int(capital / (price * 100))

        payload = {
          "orderStrategyType": "TRIGGER",
          "session": "NORMAL",
          "duration": "DAY",
          "orderType": "LIMIT",
          "price": price,
          "orderLegCollection": [
            {
              "instruction": "BUY_TO_OPEN",
              "quantity": quantity,
              "instrument": {
                "assetType": "OPTION",
                "symbol": symbol
              }
            }
          ],
          "childOrderStrategies": [
            {
              "orderStrategyType": "OCO",
              "childOrderStrategies": [
                {
                  "orderStrategyType": "SINGLE",
                  "session": "NORMAL",
                  "duration": "DAY",
                  "orderType": "LIMIT",
                  "price": limit,
                  "orderLegCollection": [
                    {
                      "instruction": "SELL_TO_CLOSE",
                      "quantity": quantity,
                      "instrument": {
                        "assetType": "OPTION",
                        "symbol": symbol
                      }
                    }
                  ]
                },
                {
                  "orderStrategyType": "SINGLE",
                  "session": "NORMAL",
                  "duration": "DAY",
                  "orderType": "STOP",
                  "stopPrice": stop,
                  "orderLegCollection": [
                    {
                      "instruction": "SELL_TO_CLOSE",
                      "quantity": quantity,
                      "instrument": {
                        "assetType": "OPTION",
                        "symbol": symbol
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }

        r = http.post(url=self.order_url, headers=self.auth.header(), json=payload,
            timeout=self.timeout)
        return bool(r.status_code == 201)

    @staticmethod
    def to_full_symbol(ticker, exp, putCall, strike):
        d = parse(exp)
        if 'call' in putCall.lower():
            t = 'C'
        elif 'put' in putCall.lower():
            t = 'P'
        # else wtf man
        # TODO raise exception

        return f"{ticker.upper()}_{dt.strftime(d, '%m%d%y')}{t}{int(strike)}"
