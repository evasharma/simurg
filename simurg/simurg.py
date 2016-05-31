from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2


def get_top_story_links(base_url):
    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('div.topic a')
    hrefs = [link.get('href') for link in links]
    links = [urljoin(base_url, href) for href in hrefs]
    return links


def extract_news_links(top_story_links, base_url):
    story_link_map = dict()
    for top_story_link in top_story_links:
        links = []
        response = urllib2.urlopen(top_story_link)
        h = response.read()
        s = BeautifulSoup(h, 'html.parser')
        news = s.select("div.blended-wrapper.esc-wrapper")
        for news in news:
            link = news.select('h2.esc-lead-article-title a')[0]
            time = news.select('td.al-attribution-cell.timestamp-cell span.al-attribution-timestamp')
            headline = news.select('span.titletext')
            print(headline[0].text)
            for t in time:
                print '*'*10
                print t.text
            links.append(link.get('url'))
        story_link_map[top_story_link.text] = links
    return story_link_map


base_url = 'http://news.google.com/news'


def extract_news(base_url):
    top_story_links = get_top_story_links(base_url)
    print(top_story_links)
    # my_map = extract_news_links(top_story_links, base_url)
    # for k, v in my_map.iteritems():
    #    print u'{}: #{} Links'.format(k, len(v))


extract_news(base_url)
