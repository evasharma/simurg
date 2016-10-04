from selector_finder import find_selector
from dragnet import content_extractor
from collections import OrderedDict
from unidecode import unidecode
from bs4 import BeautifulSoup
from clients.fetcher import fetch
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
    headline = headline[:-4]
    if ':' in headline:
        headline = headline.split(':')[1]
    elems = soup(text=re.compile(re.escape(headline)))
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
        fetch_url = news['wayback_url']
    else:
        fetch_url = news['url']
    if not redis_client.exists(news['url']):
        news['html'] = fetch(fetch_url)
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
    if lang == 'fr':
        return 'https://news.google.com/news?ned=fr'
    if lang == 'it':
        return 'https://news.google.com/news?ned=it'
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
        if value['wayback_url'] == 'None':
            html = fetch(value['url'])
        else:
            html = fetch(value['wayback_url'])
        time.sleep(1)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            continue
        headline_elems = soup.select(value['headline_selector'], None)
        if len(headline_elems) > 0:
            headline = headline_elems[0].text.strip()
        else:
            logging.debug('Headline can not be refound: url={}, selector={}'
                          .format(value['url'], value['headline_selector']))
            continue
        news = OrderedDict()
        news['id'] = value['id']
        news['timestamp'] = value['timestamp']
        news['lang'] = redis_client.lang
        news['url'] = value['url']
        news['wayback_url'] = value['wayback_url']
        news['headline'] = headline.strip()
        news['body'] = content_extractor.analyze(html).strip()
        yield news
