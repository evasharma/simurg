import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False


def fetch(url, max_attempts=2, timeout=5):
    import requests
    import socket
    import time
    """Downloads a URL.
    Args:
        url: The URL.
        max_attempts: Max attempts for downloading the URL.
        timeout: Connection timeout in seconds for each attempt.
    Returns:
        The HTML at the URL or None if the request failed.
    """

    attempts = 0

    while attempts < max_attempts:
        try:
            req = requests.get(
                url, allow_redirects=False, timeout=timeout)

            if req.status_code == requests.codes.ok:
                content = req.text
                logger.info('Success fetching url {}'.format(url))
                return content
            elif (req.status_code in [301, 302, 404, 503] and
                  attempts == max_attempts - 1):
                pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except socket.timeout:
            pass

        time.sleep(2)
        attempts += 1
    # ToDo: Add logging
    return None
