from template import get_base_url, append_html, append_headline_selector
from urlparse import urlparse, parse_qs
from news_builder import build_news
from util import is_valid
import scrapper
import template
import logging


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
        logging.info('Processing story "{}"'.format(story[0]))
        for news in build_news(url, base_url):
            news = append_html(news)
            news = append_headline_selector(news)
            if is_valid(news, field='headline_selector'):
                template.redis_client.insert(news)
