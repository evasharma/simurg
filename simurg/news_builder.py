from bs4 import BeautifulSoup
import uuid
from fetcher import fetch
import scrapper
from wayback import get_wayback_url


def build_news(top_story_link, base_url):
    top_story_html = fetch(top_story_link)
    soup = BeautifulSoup(top_story_html, 'html.parser')
    news_elements = scrapper.get_news_elements(soup)
    for news_el in news_elements:
        news = {}
        news['id'] = unicode(uuid.uuid4())
        news['headline'] = scrapper.get_news_headline(news_el).text
        news['url'] = scrapper.get_news_link(news_el).get('href')
        print('Before')
        news['wayback_url'] = get_wayback_url(news['url'])
        print('After')
        yield news
