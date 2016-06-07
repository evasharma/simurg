import logging
from news_builder import build_news
from selector_finder import el_to_css_selector
import scrapper
from fetcher import fetch
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from redis_client import RedisClient


redis_client = RedisClient()


def find_headline_element(soup, headline):
    elems = soup(text=re.compile(re.escape(headline[:-4])))
    el = elems[0].parent if len(elems) > 0 else None
    if el and len(el.text.strip()) > 0:
        logging.debug('found headline element on the page')
        return el
    logging.debug('headline "{}" not found'.format(unidecode(headline)))
    return None


def append_html(news):
    if is_valid(news, field='wayback_url'):
        if not redis_client.exists(news['url']):
            news['html'] = fetch(news['wayback_url'])
            return news
    logging.info('Skipping duplicate url: {}'.format(news['url']))
    return news


def append_selector(news):
    if is_valid(news, field='html'):
        soup = BeautifulSoup(news['html'], 'html.parser')
        headline_el = find_headline_element(soup, news['headline'])
        if headline_el:
            news['headline_selector'] = el_to_css_selector(soup, headline_el)
            logging.debug('found selector: {}'.format(news['headline_selector']))
            return news
        logging.debug('css selector could not be found!')
    return news


def is_valid(news, field=None):
    try:
        news[field]
    except:
        logging.debug('field {} is not valid'.format(field))
        return False
    if news[field]:
        logging.debug('field {} is  valid'.format(field))
        return True
    logging.debug('field {} is not valid'.format(field))
    return False


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


def create_corpus(lang='de'):
    base_url = get_base_url(lang=lang)
    story_urls = scrapper.get_story_urls(base_url)
    for top_story_link in story_urls:
        for news in build_news(top_story_link, base_url):
            news = append_html(news)
            append_selector(news)
            if is_valid(news, field='headline_selector'):
                redis_client.insert(news)
