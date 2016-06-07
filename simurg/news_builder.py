from wayback import get_wayback_url
from bs4 import BeautifulSoup
from fetcher import fetch
import scrapper
import uuid


def build_news(url, base_url):
    """Constructs the first version of a news that hat to be completed later.
    A news consists of the following fields:
        id, headline, url, wayback_url

    # Arguments
        url: top story page that contains the news
        base_url: base google news page

    # Returns
        news: a news dictionary objects
    """
    soup = BeautifulSoup(fetch(url), 'html.parser')
    news_elements = scrapper.get_news_elements(soup)
    for news_el in news_elements:
        news = {}
        news['id'] = unicode(uuid.uuid4())
        news['headline'] = scrapper.get_news_headline(news_el).text
        news['url'] = scrapper.get_news_link(news_el).get('href')
        news['wayback_url'] = get_wayback_url(news['url'])
        yield news
