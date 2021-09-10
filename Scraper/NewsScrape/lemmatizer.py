import ujson as json
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from re import search
import math
import gensim
import xml.etree.cElementTree as ET
from progressbar import ProgressBar


def stem_lemamtize(links):
    print('Converting pages to vector representation...')
    # links is a list of links, that can have just one link if user selected by title
    tokenized = get_tagged_from_json(links)

    # lemmatize
    lemmas_per_article = []
    pbar = ProgressBar()
    print("Stem and lemmatize articles....")
    for doc in pbar(tokenized):
            lemmas_per_article.append(get_lemmas(doc))
    with open('Results/lemmas.json', 'w')as lemmas_out:
        json.dump(dict(zip(range(len(tokenized)), lemmas_per_article)), lemmas_out)

    print('Sucessfully extracted lemmas. A full list of them can be found in Results/lemmas.json')

    # create gensim dictionary and appearances of lemmas in dictionary
    thesaurus_dict = gensim.corpora.Dictionary(lemmas_per_article)
    article_corpus = [thesaurus_dict.doc2bow(doc) for doc in lemmas_per_article]

    return thesaurus_dict, article_corpus


def get_tagged_from_json(links):
    # gets the tagged articles from local files
    with open('Results/pos_tags.json') as jsonfile:
        tagged_dict = json.load(jsonfile)

    # tagged dict μορφη <link> : <[[token, pos], [token, pos]...>
    tokenized = []
    tagged_dict = remove_closedclasscategories(tagged_dict)
    print('Saving new vector format....')
    # save the new article
    with open('Results/pos_tags_noclosed.json', 'w')as json_out:
        json.dump(tagged_dict, json_out)
    print('Vector format saved and can be found in Results/pos_tags_noclosed.json.')
    l = [''.join(i) for i in links]
    for key in tagged_dict:
        doc = []
        if key not in l:
            continue
        else:
            for pair in tagged_dict[key]:
                if len(pair) == 0:
                    doc.append("a")
                    continue
                doc.append(pair[0])
            if len(doc) > 0:
                tokenized.append(doc)

    return tokenized


def remove_closedclasscategories(tagged_dic):
    closedclasscategories = ['.', ',', ':', 'CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', ".", ",", ":", "D" "C" "T" "X" "N" "S" "D" "DT" "OS" "RP" "RP$" "P" "O" "H" "DT" "P" "P$" "RB"]
    for key in tagged_dic:
        article = tagged_dic[key]
        for pair in article:
            if pair[1] in closedclasscategories:
                pair.clear()
        tagged_dic[key] = article
    return tagged_dic


def get_lemmas(data):
    # stem and lemmatize
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer('english')
    lemmas = []
    for text in data:
        lemmas.append(stemmer.stem(lemmatizer.lemmatize(text, pos='v')))

    # remove single character lemmas
    for lemma in lemmas:
        if len(lemma) < 3:
            lemmas.remove(lemma)
    # remove duplicates
    lemmas = list(dict.fromkeys(lemmas))
    for lemma in lemmas:
        if lemma not in nltk.corpus.words.words():
            lemmas.remove(lemma)
    return lemmas
