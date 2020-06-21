import requests
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout, Timeout
import time

from utils.const import RETRY_REQUEST_TIME, RETRIES_QNT


def exception_retry(repeats=RETRIES_QNT, delay_sec=RETRY_REQUEST_TIME) -> \
        object or Exception:
    """
    Retry decorator
    :param repeats: num of time to repeat
    :param delay_sec: amount of seconds to wait after each execution
    :return: function
    """

    def wrapper(f):
        def wrapped(*args, **kwargs):
            for _ in range(repeats):
                response = f(*args, **kwargs)
                if isinstance(response, requests.Response):
                    return response
                time.sleep(delay_sec)
            print("No connection")
            raise Exception
        return wrapped
    return wrapper


# @exception_retry
def req_request(method: str, **kwargs) -> object:
    """
    Method for handling errors during single request
    :param method: HTTP method
    :param kwargs: request keyword arguments
    :return: http response
    """
    time.sleep(0.5)
    try:
        response = requests.request(method=method, **kwargs, timeout=3)
        return response
    except (ConnectTimeout, HTTPError, ReadTimeout,
            Timeout, ConnectionError) as exception:
        print(f'Error: No connection, detail: {exception}')
