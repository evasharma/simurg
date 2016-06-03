import requests
import logging
import time
import re


wayback_pattern = re.compile(r'web/([^/]*)/')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False

def get_wayback_url(url):
    """Retrieves the URL for the latest historic copy using Wayback Machine.
    Args:
      urls: The URL for a specific page (canonical URL + forwarding URL's).
      max_attempts: The maximum attempts at requesting the URL.
    Returns:
      The URL or None if no copy is stored for the URL.
    Raises:
      RuntimeError: Failed to retrieve the URL.
    """

    if not url:
        return None

    index_collection_url = 'http://archive.org/wayback/available'

    payload = {'url': url}

    try:
        entry_req = requests.get(index_collection_url, params=payload,
                                 allow_redirects=False)

        if entry_req.status_code != requests.codes.ok:
            logger.info('failed retrieving the wayback url for: {}'.format(url))
            return None

        entry = entry_req.json()

        if 'closest' not in entry['archived_snapshots']:
            logger.info('failed retrieving the wayback url for: {}'.format(url))
            return None

        wayback_url = entry['archived_snapshots']['closest']['url']
        wayback_url = wayback_pattern.sub(r'web/\g<1>id_/', wayback_url, 1)
        logger.info('retrieved the wayback url for: {}'.format(url))

        return wayback_url

    except requests.exceptions.ConnectionError:
        logger.info('failed retrieving the wayback url for: {}'.format(url))
        return None

    logger.info('failed retrieving the wayback url for: {}'.format(url))
    return None
