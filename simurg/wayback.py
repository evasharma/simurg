import requests
import re
import time


wayback_pattern = re.compile(r'web/([^/]*)/')


def wayback_url(url, max_attempts=6):
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

    attempts = 0

    while attempts < max_attempts:
        try:
            entry_req = requests.get(index_collection_url, params=payload,
                                     allow_redirects=False)

            if entry_req.status_code != requests.codes.ok:
                return wayback_url(url, max_attempts)

            entry = entry_req.json()

            if 'closest' not in entry['archived_snapshots']:
                return wayback_url(url, max_attempts)

            wayback_url = entry['archived_snapshots']['closest']['url']
            wayback_url = wayback_pattern.sub(r'web/\g<1>id_/', wayback_url, 1)
            return wayback_url

        except requests.exceptions.ConnectionError:
            pass

        # Exponential back-off.
        time.sleep(math.pow(2, attempts))
        attempts += 1

    raise RuntimeError(
        'Failed to download URL for %s after %d attempts. Please run the script '
        'again.' %
        (url, max_attempts))
