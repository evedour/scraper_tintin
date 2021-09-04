import nltk
import cleaner
import MySQLdb


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
    for link, article in  content:
        # remove tab, newlines etc
        article = cleaner.clean_link(article)
        # save links
        # TODO: is this needed?
        links.append(link)
        # use nltk to tokenize and tag article
        tokens = nltk.word_tokenize(article)
        tagged = nltk.pos_tag(tokens)
        # TODO: remove punctuation
        entities = nltk.chunk.ne_chunk(tagged)
        # TODO: Save tokenized and tagged articles
        print('')
    print('')