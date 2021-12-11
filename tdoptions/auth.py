import os
import sys
from .http import post

def token():
    """
    Generate a bearer token returned as a string.

    CLIENT_ID and REFRESH_TOKEN environment variables are used
    to auth
    :return: Bearer token
    :rtype: string
    """

    # load creds
    try:
        refresh_token = os.environ['REFRESH_TOKEN']
        client_id = os.environ['CLIENT_ID']
    except KeyError as e:
        print(f'{e} environment variable not found')
        sys.exit(1)

    payload = {'grant_type': 'refresh_token',
               'refresh_token': refresh_token,
               'client_id': client_id}

    # load settings
    auth_url = os.getenv('TD_AUTH_URL', 'https://api.tdameritrade.com/v1/oauth2/token')
    timeout  = int(os.getenv('TD_TIMEOUT', '30'))

    resp = post(auth_url, data=payload, timeout=timeout)
    try:
        _token = resp.json()['access_token']
    except KeyError as e:
        print(f'{e} missing from response')
        sys.exit(1)
    return _token

def header():
    """
    Generate a bearer token returned in Authorization header format.

    :return: HTTP Authorization header
    :rtype: dict
    """

    return {'Authorization': 'Bearer ' + token()}
