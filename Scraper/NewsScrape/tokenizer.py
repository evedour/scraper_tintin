import nltk
import cleaner
import MySQLdb
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re


def insert_tokenized(tokens, key):
    # insert tokenized article to db
    tokenized_article = ""
    for token in tokens:
        tokenized_article += f'{token} '
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    crs = db.cursor()
    # care for typo in column
    crs.execute(f"""UPDATE articles SET tokenized_aricle = \"{tokenized_article}\" WHERE id = \"{key}\"""")
    db.commit()


def get_articles():
    # connect to phpmyadmin and get links and articles
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    crs = db.cursor()
    crs.execute("""SELECT link, article FROM articles""")

    return crs.fetchall()


def tokenize():
    # get articles from localhost db
    content = get_articles()
    tokenized_articles = []
    links = []
    punctuations = "?:!.,;"
    keys = ['token', 'tag']
    for link, article in content:
        print(f'Tokenizing {link}')
        # remove tab, newlines etc
        article = cleaner.clean_link(article)
        # save links
        links.append(link)
        # use nltk to tokenize and tag article
        article = article.lower()
        article = article.replace('{html}', "")
        cleans = re.compile('<.*?>')
        cleantext = re.sub(cleans, '', article)
        rem_url = re.sub(r'http\S+', '', cleantext)
        rem_num = re.sub('[0-9]+', '', rem_url)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(rem_num)
        insert_tokenized(tokens, link)
        no_stopwords = [word.lower() for word in tokens if not word in stopwords.words()]
        tagged = nltk.pos_tag(no_stopwords)
        entities = nltk.chunk.ne_chunk(tagged)
        tokenized_articles.append(tagged)

    # save tokenized and tagged articles in json format (link: [('token','tag'),....])
    with open('Results/pos_tags.json', 'w') as output:
        json.dump(dict(zip(links, tokenized_articles)), output)
        output.close
    print('Tokenized and tagged articles can be found under Results in pos_tags.json')

