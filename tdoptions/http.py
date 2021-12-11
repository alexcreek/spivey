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
            resp.raise_for_status() # Raise HTTPError for 4xx and 5xx responses
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            #TODO use a logger
            print(e)
            if retries == 1:
                sys.exit(1)
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
            resp.raise_for_status() # Raise HTTPError for 4xx and 5xx responses
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            #TODO use a logger
            print(e)
            if retries == 1:
                sys.exit(1)
        retries -= 1
        backoff += 1
        sleep(backoff)
    return resp