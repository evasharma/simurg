#!/usr/bin/env python
# -*- coding: utf-8 -*-

from template import get_base_url, append_html, append_headline_selector
from urlparse import urlparse, parse_qs
from redis_client import RedisClient
from news_builder import build_news
from util import is_valid
import scrapper
import template
import logging
import time
import json
import sys
import io
reload(sys)
sys.setdefaultencoding("utf-8")


def create_template_corpus(lang='de'):
    """Creates a template corpus where for each news url, the headline css
    selector and wayback_url of the news is stored.

    # Arguments:
        lang: language of the corpus
    """
    redis_client = RedisClient(lang=lang)
    base_url = get_base_url(lang=lang)
    while True:
        story_urls = scrapper.get_story_urls(base_url)
        for url in story_urls:
            story = parse_qs(urlparse(url).query, keep_blank_values=True)['q']
            story = unicode(story[0])
            logging.info('Processing story "{}"'.
                         format((story.decode('utf-8'))))
            for news in build_news(url):
                if news:
                    news = append_html(news, redis_client)
                    news = append_headline_selector(news)
                    if is_valid(news, field='headline_selector'):
                        redis_client.insert(news)
                    else:
                        logging.debug('Ignoring invalid news with url: {}'.
                                      format(news['url']))
        time.sleep(300)


def populate_template_corpus(lang='de'):
    """Populates the news with required fields and write them to json files.
    For each news object a json file which has the id of news is created

    # Arguments:
        lang: language of the corpus
    """
    redis_client = RedisClient(lang=lang)
    for news in template.populate(redis_client):
        if not is_valid(news, field='headline'):
            continue
        base = 'docs/' + lang + '/'
        filename = base + news['id'] + '.json'
        with io.open(filename, 'w', encoding='utf8') as json_file:
            data = json.dumps(news,
                              ensure_ascii=False,
                              encoding='utf8',
                              indent=4)
            logging.info('Wrote document to disk: id={}'.format(news['id']))
            json_file.write(unicode(data))
