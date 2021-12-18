import os
import sys
from datetime import datetime as dt
from datetime import timedelta, timezone
from .http import post

class Auth():
    def __init__(self):
        self.ttl = 0
        self._token = None

        # load creds
        try:
            self.refresh_token = os.environ['REFRESH_TOKEN']
            self.client_id = os.environ['CLIENT_ID']
        except KeyError as e:
            print(f'{e} environment variable not found')
            sys.exit(1)

        self.payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id
        }

        # load settings
        self.auth_url = os.getenv('TD_AUTH_URL', 'https://api.tdameritrade.com/v1/oauth2/token')
        self.timeout = int(os.getenv('TD_TIMEOUT', '30'))

    def token(self):
        """
        Generate a bearer token returned as a string.

        CLIENT_ID and REFRESH_TOKEN environment variables are used to authenticate
        :return: Bearer token
        :rtype: string
        """
        if self.ttl:
            if self.ttl > dt.now(timezone.utc):
                return self._token

        resp = post(self.auth_url, data=self.payload, timeout=self.timeout)
        payload = resp.json()
        try:
            _token = payload['access_token']
            expiration = payload['expires_in']
        except KeyError as e:
            print(f'{e} missing from response')
            sys.exit(1)
        self.ttl = dt.now(timezone.utc) + timedelta(seconds=expiration)
        self._token = _token
        return self._token

    def header(self):
        """
        Generate a bearer token returned in Authorization header format.

        :return: HTTP Authorization header
        :rtype: dict
        """
        return {'Authorization': 'Bearer ' + self.token()}
