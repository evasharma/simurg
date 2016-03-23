from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2


def get_top_stories(base_url):
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('div.topic a')
    return links


def extract_news_links(top_stories, base_url):
    story_link_map = dict()
    for story in top_stories:
        links = []
        my_url = urljoin(base_url, story.get('href'))
        response = urllib2.urlopen(my_url)
        h = response.read()
        s = BeautifulSoup(h, 'html.parser')
        news = s.select("div.blended-wrapper.esc-wrapper")
        for news in news:
            link = news.select('h2.esc-lead-article-title a')[0]
            time = news.select('td.al-attribution-cell.timestamp-cell span.al-attribution-timestamp')
            for t in time:
                print '*'*10
                print t.text
            links.append(link.get('url'))
        story_link_map[story.text] = links
    return story_link_map


base_url = 'http://news.google.com/news'


def extract_news(base_url):
    top_stories = get_top_stories(base_url)
    my_map = extract_news_links(top_stories, base_url)
    for k, v in my_map.iteritems():
        print u'{}: #{} Links'.format(k, len(v))


extract_news(base_url)
