from bs4 import BeautifulSoup
import string
import re
import requests


def get_politico():
    with open('Results/news_www.politico.eu.html', 'rb')as politico:
        soup = BeautifulSoup(politico, 'html.parser')
    titles  = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next
        link = link.replace('\r', '')
        link = ''.join(link.strip().split('\\n'))
        link.replace('\\', '')
        encoded = item.findAll(text=True)
        content = []
        for cd in encoded:
            if "<p>" in cd:
                content.append(cd)
        article = ", ".join(content)
        article = re.sub('<.*?>', '', article)
        article = ''.join(article.strip().split('\\n'))
        article.replace('\\', '')
        article = re.sub('/', '  ', article)
        articles.append(article)
        titles.append(title)
        links.append(link)
    return titles, links, articles


def get_euronews():
    with open('Results/news_en.html', 'rb')as euronews:
        soup = BeautifulSoup(euronews, 'html.parser')
    titles = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next
        # replacing link breaks (\r, \n) because requests can't handle them
        link = link.replace('\r', '')
        link = ''.join(link.strip().split('\\n'))
        link.replace('\\', '')
        # get article
        r = requests.get(link)
        good_soup = BeautifulSoup(r.content, 'html.parser')
        article = []
        divs = good_soup.find_all('div', class_ = 'c-article-content')
        # get the actual article, paragraph by paragraph
        for div in divs:
            for p in div.find_all('p'):
                article.append(p.text)
        content = ", ".join(article)
        titles.append(title)
        links.append(link)
        articles.append(content)
    return titles, links, articles


def get_washington_post():
    print('Done: Washington Post')


def get_bbc():
    print('Done: BBC')


def get_html_text():
    politico_titles, politico_links, politico_articles = get_politico()
    euronews_titles, euronews_links, euronews_articles = get_euronews()
    print('')
    # get_washington_post()
    # get_bbc()
