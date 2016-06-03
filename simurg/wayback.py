import requests
import re


wayback_pattern = re.compile(r'web/([^/]*)/')


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
            return get_wayback_url(url)

        entry = entry_req.json()

        if 'closest' not in entry['archived_snapshots']:
            return get_wayback_url(url)

        wayback_url = entry['archived_snapshots']['closest']['url']
        wayback_url = wayback_pattern.sub(r'web/\g<1>id_/', wayback_url, 1)
        return wayback_url

    except requests.exceptions.ConnectionError:
        return None

    return None
