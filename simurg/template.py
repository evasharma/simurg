from selector_finder import find_selector
from redis_client import RedisClient
from unidecode import unidecode
from bs4 import BeautifulSoup
from fetcher import fetch
from util import is_valid
import logging
import re


redis_client = RedisClient()


def clean_soup(soup):
    """Removes some elements that may negatively affect the
    quality of headline extraction

    # Arguments
        soup: parsed html document
    """
    exclude_tags = ['style', 'script', '[document]', 'head', 'title']
    [s.extract() for s in soup(exclude_tags)]


def find_headline_element(soup, headline):
    """Finds the headline element on a page based on a headline hint.

    # Argument
        soup: parsed html page
        headline: headline hint to be used

    # Returns
        el: headline element (None if not found)
    """
    clean_soup(soup)
    # headline sometimes contains "..." at the end. We eliminate it.
    elems = soup(text=re.compile(re.escape(headline[:-4])))
    d = {}
    for el in elems:
        d[el.parent] = el.parent.text.strip()
    headline_elems = sorted(d, key=lambda k: len(d[k]))
    if len(headline_elems) > 0:
        return headline_elems[0]
    logging.debug('Headline "{}" not found'.format(unidecode(headline)))
    return None


def append_html(news):
    """Appends an html field to the news, only if the wayback_url is valid and
    the url does not already exist in the database.

    # Arguments
        news: news object as dictionary

    # Returns
        news: news object with or without html field
    """
    if is_valid(news, field='wayback_url'):
        if not redis_client.exists(news['url']):
            news['html'] = fetch(news['wayback_url'])
            return news
        logging.info('Skipping duplicate url: {}'.format(news['url']))
    return news


def append_headline_selector(news):
    """Appends the headline css selector field to the news, only if the html
    field exists and is valid.

    # Arguments
        news: news object as dictionary

    # Returns
        news: news object with or without headline css selector field
    """
    if is_valid(news, field='html'):
        soup = BeautifulSoup(news['html'], 'html.parser')
        headline_el = find_headline_element(soup, news['headline'])
        if headline_el:
            news['headline_selector'] = find_selector(soup, headline_el)
            return news
        logging.debug('Headline css selector could not be found!')
    return news


def get_base_url(lang='de'):
    """ Return the google news url for a specific language

    # Arguments
        lang: required language for google news
    # Returns
        url: corresponding google news url for the given language
    """
    if lang == 'de':
        return 'https://news.google.de/'
    else:
        raise ValueError('unsupported language {}'.format(lang))
