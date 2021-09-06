import json
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from re import search


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    # return noun in order for it to actually work (original solution was None, but at runtime threw KeyError)


def vectorize(links):
    print('Converting pages to vector representation')
    # links is a list of links, that can have just one link if user selected by title
    tagged_dict = get_tagged_from_json()
    tagged_dictionary = remove_closedclasscategories(tagged_dict)
    # save the new article
    with open('Results/pos_tags_noclosed.json', 'w')as json_out:
        json.dump(tagged_dictionary, json_out)
    lemmas = get_lemmas(tagged_dictionary)

    vector = []

    print('Counting lemma appearances')
    with open('Results/index.json', 'a') as vct:
        for lemma in lemmas:
            appearances = []
            for key in tagged_dictionary:
                count_in_article = 0
                for pair in tagged_dictionary[key]:
                    if len(pair) == 0:
                        continue
                    else:
                        if lemma in pair[0]:
                            isit = (lemma in pair[0])
                            count_in_article += 1
                    appearances.append((key, count_in_article))
            json.dump({f'{lemma}': f"{appearances}"}, vct)
    print('Successfully created index.json')


def get_tagged_from_json():
    with open('Results/pos_tags.json') as jsonfile:
        tagged_dict = json.load(jsonfile)
    return tagged_dict


def remove_closedclasscategories(tagged_dic):
    closedclasscategories = ['.', ',', ':', 'CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', ".", ",", ":", "D" "C" "T" "X" "N" "S" "D" "DT" "OS" "RP" "RP$" "P" "O" "H" "DT" "P" "P$" "RB"]
    for key in tagged_dic:
        article = tagged_dic[key]
        for pair in article:
            if pair[1] in closedclasscategories:
                pair.clear()
        tagged_dic[key] = article
    return tagged_dic


def get_lemmas(tagged_dictionary):
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for key in tagged_dictionary:
        for pair in tagged_dictionary[key]:
            if len(pair) == 0:
               continue
            else:
                if lemmatizer.lemmatize(pair[0]) not in lemmas:
                    lemmas.append(lemmatizer.lemmatize(pair[0], pos=get_wordnet_pos(pair[1])))

    # remove single character lemmas
    for lemma in lemmas:
        if len(lemma) == 1:
            lemmas.remove(lemma)

    # save lemmas
    with open('Results/lemmas.txt', 'w')as lemmas_out:
        for lemma in lemmas:
            lemmas_out.write(f'{lemma},')
    print('Sucessfully extracted lemmas. A full list of them can be found in Results/lemmas.txt')

    return lemmas
