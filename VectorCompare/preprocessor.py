import nltk
import re
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import gensim
from gensim.utils import simple_preprocess
from progressbar import ProgressBar


def make_tokens(text):
    tokenized_articles = []
    # use nltk to tokenize and tag article
    text = text.lower()
    text = text.replace('{html}', "")
    cleans = re.compile('<.*?>')
    cleantext = re.sub(cleans, '', text)
    rem_url = re.sub(r'http\S+', '', cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)
    no_stopwords = [word.lower() for word in tokens if not word in stopwords.words()]
    for token in no_stopwords:
        if len(token) < 4:
            no_stopwords.remove(token)
    tokenized_articles.append(no_stopwords)
    return tokenized_articles


def make_lemmas(data):
    stemmer = SnowballStemmer("english")
    lemmatized = []
    for doc in data:
        for text in doc:
            lemmatized.append(stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v')))
    lemmatized = list(dict.fromkeys(lemmatized)) # remove duplicates
    for lemma in lemmatized:
        if lemma not in nltk.corpus.words.words():
            lemmatized.remove(lemma)
    return lemmatized


def exctract_themes(collection, name):
    pbar = ProgressBar()
    # tokenizer
    lemmatized_collection = []
    for doc in pbar(collection):
        tokenized = make_tokens(doc)
        lemmatized = make_lemmas(tokenized)
        lemmatized_collection.append(lemmatized)

    return lemmatized_collection
