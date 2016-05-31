from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import pprint
import uuid


def get_top_story_links(base_url):
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('div.topic a')
    hrefs = [link.get('href') for link in links]
    links = [urljoin(base_url, href) for href in hrefs]
    return links


def extract_news_links(top_story_links, base_url):
    batch = []
    for top_story_link in top_story_links:
        top_story_html = urllib2.urlopen(top_story_link).read()
        soup = BeautifulSoup(top_story_html, 'html.parser')
        news_elements = soup.select("div.blended-wrapper.esc-wrapper")
        for news_el in news_elements:
            news = {}
            news['id'] = unicode(uuid.uuid4())
            link = news_el.select('h2.esc-lead-article-title a')[0]
            headline = news_el.select('span.titletext')[0]
            news['headline'] = headline.text
            news['url'] = link.get('href')
            batch.append(news)
    return batch


base_url = 'http://news.google.com/news'


def extract_news(base_url):
    top_story_links = get_top_story_links(base_url)
    batch = extract_news_links(top_story_links, base_url)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(batch)


extract_news(base_url)
