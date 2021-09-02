from bs4 import BeautifulSoup
import string
import re


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
    return titles, links, articles


def get_euronews():
    with open('Results/news_en.html', 'rb')as euronews:
        soup = BeautifulSoup(euronews, 'html.parser')
    print('Done: Euronews')


def get_washington_post():
    print('Done: Washington Post')


def get_bbc():
    print('Done: BBC')


def get_html_text():
    politico_titles, politico_links, politico_articles = get_politico()
    # get_euronews()
    # get_washington_post()
    # get_bbc()
