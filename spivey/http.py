import sys
from time import sleep
import requests

def get(*args, **kwargs):
    """
    Wrapper around requests.get() with retries and exception handling.

    :param *args: Args that requests.get() takes
    :param **kwargs: Keyword args that requests.get() takes
    :return: The request.get() response object
    :rtype: requests.models.Response
    """

    retries = 3
    backoff = 0
    while retries > 0:
        try:
            resp = requests.get(*args, **kwargs)
            if is_ok(resp):
                break
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            #TODO use a logger
            print(e)
            if retries == 1:
                sys.exit(1)
            print('Retrying request')
        retries -= 1
        backoff += 1
        sleep(backoff)
    return resp

def post(*args, **kwargs):
    """
    Wrapper around requests.post() with retries and exception handling.

    :param *args: Args that requests.post() takes
    :param **kwargs: Keyword args that requests.post() takes
    :return: The request.post() response object
    :rtype: requests.models.Response
    """

    retries = 3
    backoff = 0
    while retries > 0:
        try:
            resp = requests.post(*args, **kwargs)
            if is_ok(resp):
                break
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            #TODO use a logger
            print(e)
            if retries == 1:
                sys.exit(1)
            print('Retrying request')
        retries -= 1
        backoff += 1
        sleep(backoff)
    return resp

def is_ok(resp):
    """
    Check a requests.models.response for a bad status code

    :param resp: response to check
    :return: True if the status_code is normal
    :rtype: boolean
    :raises HTTPError: if the status code is 5xx or 429
    """

    bad_status_codes = [429, 500, 501, 502, 503, 504, 505, 507, 508, 510, 511]
    if resp.status_code in bad_status_codes:
        msg = f'{resp.status_code} Error for url: {resp.url}'
        raise requests.exceptions.HTTPError(msg)
    return True
