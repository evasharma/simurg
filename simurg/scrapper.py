from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import logging


TOP_STORY_LINK_SELECTOR = 'div.topic a'
NEWS_ELEMENT_SELECTOR = 'div.blended-wrapper.esc-wrapper'
NEWS_LINK_SELECTOR = 'h2.esc-lead-article-title a'
HEADLINE_SELECTOR = 'span.titletext'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False

def get_top_story_links(base_url, selector=TOP_STORY_LINK_SELECTOR):
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(selector)
    hrefs = [link.get('href') for link in links]
    links = [urljoin(base_url, href) for href in hrefs]
    logger.info('discovered {} top stories on {}'.format(len(links), base_url))
    return links


def get_news_elements(soup):
    return soup.select(NEWS_ELEMENT_SELECTOR)


def get_news_link(news_element):
    return news_element.select(NEWS_LINK_SELECTOR)[0]


def get_news_headline(news_element):
    return news_element.select(HEADLINE_SELECTOR)[0]
