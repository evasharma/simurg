#!/usr/bin/env python
import logging
from redis_client import get_redis_client
from news_builder import build_news
from selector_finder import el_to_css_selector
import scrapper
from fetcher import fetch
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False

redis = get_redis_client()


def find_headline_element(soup, headline):
    elems = soup(text=re.compile(re.escape(headline)))
    el = elems[0].parent if len(elems) > 0 else None
    if el and len(el.text.strip()) > 0:
        return el
    return None


def append_html(news):
    if not redis.exists(news['url']):
        news['html'] = fetch(news['url'])
    return news


def append_selector(news):
    soup = BeautifulSoup(news['html'], 'html.parser')
    headline_el = find_headline_element(soup, news['headline'])
    if headline_el:
        news['selector'] = el_to_css_selector(soup, headline_el)
    return news


def is_valid(news, field=None):
    try:
        news[field]
    except:
        return False
    if news[field]:
        return True
    return False


def main():
    base_url = 'https://news.google.com/'
    top_story_links = scrapper.get_top_story_links(base_url)
    for top_story_link in top_story_links:
        for news in build_news(top_story_link, base_url):
            news = append_html(news)
            if is_valid(news, field='html'):
                append_selector(news)
                if is_valid(news, field='selector'):
                    redis.hset(news['url'], 'url', news['url'])
                    redis.hset(news['url'], 'selector', news['selector'])
                    redis.hset(news['url'], 'way_url', news['wayback_url'])


if __name__ == "__main__":
    main()
