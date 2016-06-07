from bs4 import BeautifulSoup
from urlparse import urljoin
import selectors
import urllib2
import logging


def get_story_urls(base_url, selector=selectors.TOP_STORY_LINK_SELECTOR):
    """Returns all top story urls on the base google news page

    # Arguments
        base_url: base google news url
        selector: css selector to select the top story urls

    # Returns
        urls: list of stop story urls
    """
    response = urllib2.urlopen(base_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    hrefs = [el.get('href') for el in soup.select(selector)]
    urls = [urljoin(base_url, href) for href in hrefs]
    logging.info('Discovered {} stories on {}'.format(len(urls), base_url))
    return urls


def get_news_elements(soup, selector=selectors.NEWS_ELEMENT_SELECTOR):
    """Returns all news section elements from a top story page

    # Arguments
        soup: parsed top story page
        selector: css selector to select news sections

    # Returns
        els: news section elements
    """
    return soup.select(selector)


def get_news_link(news_element, selector=selectors.NEWS_LINK_SELECTOR):
    """Returns the news link inside a news section

    # Arguments
        news_element: element corresponding to a news section
        selector: css selector to select the news link

    # Returns
        el: news link element
    """
    return news_element.select(selector)[0]


def get_news_headline(news_element, selector=selectors.HEADLINE_SELECTOR):
    """Returns the headline of a news section element

    # Arguments
        news_element: element corresponding to a news section
        selector: css selector to select news headline

    # Returns
        el: element containing the news headline
    """
    return news_element.select(selector)[0]
