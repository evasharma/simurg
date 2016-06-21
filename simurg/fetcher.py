import logging
import httplib2


h = httplib2.Http(".cache")


def fetch(url):
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

    try:
        (_, content) = h.request(url, "GET")
        return content
    except StandardError:
        logging.debug('Fetching url failed: {}'.format(url))
    return None
