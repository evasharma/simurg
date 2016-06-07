#!/usr/bin/env python
import logging
from redis_client import get_redis_client
from news_builder import build_news
from selector_finder import el_to_css_selector
import scrapper
from fetcher import fetch
from bs4 import BeautifulSoup
import re


redis = get_redis_client()


def find_headline_element(soup, headline):
    elems = soup(text=re.compile(re.escape(headline[:-4])))
    el = elems[0].parent if len(elems) > 0 else None
    if el and len(el.text.strip()) > 0:
        logging.info('found headline element on the page')
        return el
    logging.info('headline was: {} but it could not be found'.format(headline))
    return None


def append_html(news):
    if not redis.exists(news['url']):
        news['html'] = fetch(news['wayback_url'])
        return news
    logging.info('Skipping duplicate url: {}'.format(news['url']))
    return news


def append_selector(news):
    soup = BeautifulSoup(news['html'], 'html.parser')
    headline_el = find_headline_element(soup, news['headline'])
    if headline_el:
        news['headline_selector'] = el_to_css_selector(soup, headline_el)
        logging.info('found selector: {}'.format(news['headline_selector']))
        return news
    logging.info('css selector could not be found!')
    return news


def is_valid(news, field=None):
    try:
        news[field]
    except:
        logging.info('field {} is not valid'.format(field))
        return False
    if news[field]:
        logging.info('field {} is  valid'.format(field))
        return True
    logging.info('field {} is not valid'.format(field))
    return False


def main():
    import logging
    from logstash_formatter import LogstashFormatterV2

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV2()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    base_url = 'https://news.google.com/'
    top_story_links = scrapper.get_top_story_links(base_url)
    for top_story_link in top_story_links:
        for news in build_news(top_story_link, base_url):
            if is_valid(news, field='wayback_url'):
                news = append_html(news)
                if is_valid(news, field='html'):
                    append_selector(news)
                    if is_valid(news, field='headline_selector'):
                        logging.info('added url: {}'.format(news['url']))
                        redis.hset(news['url'], 'url', news['url'])
                        redis.hset(news['url'], 'selector',
                                   news['headline_selector'])
                        redis.hset(news['url'], 'wayback_url',
                                   news['wayback_url'])


if __name__ == "__main__":
    main()
