from wayback import get_wayback_url
from datetime import datetime
from bs4 import BeautifulSoup
from clients.fetcher import fetch
import scrapper
import logging
import uuid


def build_news(url):
    """Constructs the first version of a news that hat to be completed later.
    A news consists of the following fields:
        id, headline, url, wayback_url

    # Arguments
        url: top story page that contains the news

    # Returns
        news: a news dictionary objects
    """
    try:
        html = fetch(url)
    except StandardError:
        logging.debug('Error fetching story page {}'.format(url))
        html = None

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_elements = scrapper.get_news_elements(soup)
        for news_el in news_elements:
            news = {}
            news['id'] = unicode(uuid.uuid4())
            news['headline'] = scrapper.get_news_headline(news_el).text
            news['url'] = scrapper.get_news_link(news_el).get('href')
            news['wayback_url'] = get_wayback_url(news['url'])
            news['timestamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            yield news
    else:
        yield None
