#!/usr/bin/env python
# -*- coding: utf-8 -*-

from template import get_base_url, append_html, append_headline_selector
from urlparse import urlparse, parse_qs
from news_builder import build_news
from util import is_valid
import scrapper
import template
import logging
import sys
import threading
reload(sys)
sys.setdefaultencoding("utf-8")


def create_template_corpus(lang='de'):
    """Creates a template corpus where for each news url, the headline css
    selector and wayback_url of the news is stored.

    # Arguments:
        lang: language of the corpus
    """
    base_url = get_base_url(lang=lang)
    story_urls = scrapper.get_story_urls(base_url)
    for url in story_urls:
        story = parse_qs(urlparse(url).query, keep_blank_values=True)['q']
        story = unicode(story[0])
        logging.info('Processing story "{}"'.format((story.decode('utf-8'))))
        for news in build_news(url, base_url):
            news = append_html(news)
            news = append_headline_selector(news)
            if is_valid(news, field='headline_selector'):
                template.redis_client.insert(news)
    threading.Timer(60, create_template_corpus).start()
    create_template_corpus(lang)


def populate_template_corpus(lang='de'):
    for news in template.populate():
        import json
        import io
        base = 'docs/' + lang + '/'
        filename = base + news['id'] + '.json'
        with io.open(filename, 'w', encoding='utf8') as json_file:
            data = json.dumps(news,
                              ensure_ascii=False,
                              encoding='utf8',
                              indent=4)
            json_file.write(unicode(data))
