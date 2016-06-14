from selector_finder import find_selector
from dragnet import content_extractor
from collections import OrderedDict
from unidecode import unidecode
from bs4 import BeautifulSoup
from fetcher import fetch
from util import is_valid
import logging
import os.path
import time
import re


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
        return headline_elems
    logging.debug('Headline "{}" not found'.format(unidecode(headline)))
    return None


def append_html(news, redis_client):
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
        headline_elems = find_headline_element(soup, news['headline'])
        if headline_elems:
            news['headline_selector'] = find_selector(soup, headline_elems)
            return news
        logging.debug('Headline css selector could not be found!')
    else:
        logging.debug('Fetching html page failed. url={}'.
                      format(news['url']))
    return news


def get_base_url(lang='de'):
    """Return the google news url for a specific language

    # Arguments
        lang: required language for google news

    # Returns
        url: corresponding google news url for the given language
    """
    if lang == 'de':
        return 'http://news.google.com/news?ned=de'
    if lang == 'en':
        return 'http://news.google.com/news?ned=us'
    else:
        raise ValueError('unsupported language {}'.format(lang))


def populate(redis_client):
    """Populates the entries in the database with fields such as headline,
    body, html and url

    # Arguments
        lang: language of the database

    # Returns
        news: news objects populated with required fields
    """
    keys = redis_client.keys()
    folder = 'docs/{}/'.format(redis_client.lang)
    for key in keys:
        value = redis_client.get(key)
        f = folder + value['id'] + '.json'
        if os.path.isfile(f):
            logging.info('Skipping existing document: {}'.format(f))
            continue
        html = fetch(value['wayback_url'])
        time.sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
        headline_elems = soup.select(value['headline_selector'], None)
        headline = headline_elems[0].text.strip()
        news = OrderedDict()
        news['id'] = value['id']
        news['timestamp'] = value['timestamp']
        news['lang'] = redis_client.lang
        news['url'] = value['url']
        news['wayback_url'] = value['wayback_url']
        news['headline'] = headline
        news['body'] = content_extractor.analyze(html)
        news['html'] = html
        yield news
