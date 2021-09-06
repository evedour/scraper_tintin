import nltk
import cleaner
import MySQLdb
import json
from nltk.corpus import stopwords


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
        # remove tab, newlines etc
        article = cleaner.clean_link(article)
        # save links
        links.append(link)
        # use nltk to tokenize and tag article
        tokens = nltk.word_tokenize(article)
        for tkn in tokens:
            if tkn in punctuations:
                tokens.remove(tkn)
        no_stopwords = [word.lower() for word in tokens if not word in stopwords.words()]
        tagged = nltk.pos_tag(no_stopwords)
        entities = nltk.chunk.ne_chunk(tagged)
        tokenized_articles.append(tagged)

    # save tokenized and tagged articles in json format (link: [('token','tag'),....])
    with open('Results/pos_tags.json', 'w') as output:
        json.dump(dict(zip(links, tokenized_articles)), output)
        output.close
    print('')

