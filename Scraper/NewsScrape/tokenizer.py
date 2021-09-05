import nltk
import cleaner
import MySQLdb
import json


def get_articles():
    # connect to phpmyadmin and get links and articles
    db = MySQLdb.connect('localhost', 'root', '', 'articleDB', charset='utf8')
    cursor = db.cursor()
    cursor.execute("""SELECT link, article FROM articles""")
    return cursor.fetchall()


def tokenize():
    # get articles from localhost db
    content = get_articles()
    tokenized_articles = []
    links = []
    keys = ['token', 'tag']
    for link, article in content:
        # remove tab, newlines etc
        article = cleaner.clean_link(article)
        # save links
        links.append(link)
        # use nltk to tokenize and tag article
        tokens = nltk.word_tokenize(article)
        tagged = nltk.pos_tag(tokens)
        # TODO: remove punctuation
        entities = nltk.chunk.ne_chunk(tagged)
        tokenized_articles.append(tagged)

    with open('Results/pos_tags.json', 'w') as output:
        json.dump(dict(zip(links, tokenized_articles)), output)
        output.close
    print('')
