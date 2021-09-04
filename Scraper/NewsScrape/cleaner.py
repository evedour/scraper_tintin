from bs4 import BeautifulSoup
import string
import re
import requests
import MySQLdb
import time


def clean_link(link):
    link = link.replace('\r', '')
    link = link.replace('\t', '')
    link = link.strip()
    link = ''.join(link.strip().split('\\n'))
    link.replace('\\', '')
    return link


def get_politico():
    with open('Results/news_www.politico.eu.html', 'rb')as politico:
        soup = BeautifulSoup(politico, 'html.parser')
    titles  = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next # needs next because it appears as link/ (not link) in the soup
        link = clean_link(link)
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
        link = clean_link(link)
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


def get_bbc():
    with open('Results/news_news.html', 'rb')as bbc_news:
        soup = BeautifulSoup(bbc_news, 'html.parser')
    titles = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next
        r = requests.get(link)
        good_soup = BeautifulSoup(r.content, 'html.parser')
        article = []
        for article_tag in good_soup.find_all('article', class_="ssrcss-xalfp3-ArticleWrapper e1nh2i2l6"):
            for div in article_tag.find_all('div', class_='ssrcss-uf6wea-RichTextComponentWrapper e1xue1i87'):
                for p in div.find_all('p'):
                    article.append(p.text)
        content = ",".join(article)
        articles.append(content)
        titles.append(title)
        links.append(link)
    return titles, links, articles


def get_aljazeera():
    with open('Results/news_xml.html', 'rb')as AJ:
        soup = BeautifulSoup(AJ, 'html.parser')
    titles = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = item.link.next
        r = requests.get(clean_link(link))
        good_soup = BeautifulSoup(r.content, 'html.parser')
        article = []
        for div in good_soup.find_all('div', class_='wysiwyg wysiwyg--all-content css-1vsenwb'):
            for p in div.find_all('p'):
                article.append(p.text)
        content = ', '.join(article)
        articles.append(content)
        titles.append(title)
        links.append(link)

    return titles, links, articles


def get_eureporter():
    with open('Results/news_www.eureporter.co.html', 'rb') as eureporter:
        soup = BeautifulSoup(eureporter, 'html.parser')
    titles = []
    links = []
    articles = []
    items = soup.find_all('item')
    for item in items:
        title = item.title.text
        link = clean_link(item.link.next)
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


def get_html_text():

    print(f'Starting parse: Politico')
    politico_titles, politico_links, politico_articles = get_politico()
    print(f'Saving to database...')
    save_to_db('politico', politico_titles, politico_links, politico_articles)

    print(f'Starting parse: Euronews')
    euronews_titles, euronews_links, euronews_articles = get_euronews()
    print(f'Saving to database...')
    save_to_db('euronews', euronews_titles, euronews_links, euronews_articles)

    print(f'Starting parse: BBC News')
    bbc_titles, bbc_links, bbc_articles = get_bbc()
    print(f'Saving to database...')
    save_to_db('bbc', bbc_titles,bbc_links,bbc_articles)

    print(f'Starting parse: Aljazeera')
    aj_titles, aj_links, aj_articles = get_aljazeera()
    print(f'Saving to database...')
    save_to_db('aljazeera', aj_titles,aj_links,aj_articles)

    print(f'Starting parse: Eureporter')
    eureporter_titles, eureporter_links, eureporter_articles = get_eureporter()
    print(f'Saving to database...')
    save_to_db('eureporter', eureporter_titles,eureporter_links,eureporter_articles)

    print('All articles inserted to database and can be found in localhost')

def save_to_db(source, titles, links, articles):
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    insertrec = db.cursor()

    for title in titles:
        tlt = title.replace("'", '"')
        # get article on title's index, encoded and decoded to ignore ascii characters
        article = articles[titles.index(title)].replace("'", '"').encode("ascii", "replace").decode()
        sqlquery = f'insert into articles(source,title,link,article) values(\'{source}\', \'{tlt}\',\'{links[titles.index(title)]}\',\'{article}\')'
        insertrec.execute(sqlquery)
