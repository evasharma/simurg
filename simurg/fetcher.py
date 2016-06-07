import logging
import requests
import socket
import time


def fetch(url, max_attempts=2, timeout=5):
    """Downloads a URL.
    Args:
        url: The URL.
        max_attempts: Max attempts for downloading the URL.
        timeout: Connection timeout in seconds for each attempt.
    Returns:
        The HTML at the URL or None if the request failed.
    """
    if not url:
        return None

    attempts = 0

    while attempts < max_attempts:
        try:
            req = requests.get(
                url, allow_redirects=False, timeout=timeout)

            if req.status_code == requests.codes.ok:
                content = req.text
                logging.info('fetched url: {}'.format(url))
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
    logging.info('fetching url fail: {}'.format(url))
    return None
