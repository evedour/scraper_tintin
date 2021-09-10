import ujson as json
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import wordnet
from re import search
import math
import xml.etree.cElementTree as ET


def get_wordnet_pos(treebank_tag):
    # convert pos tag to wordnet pos tag
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


def indexer(links):
    print('Converting pages to vector representation')
    # links is a list of links, that can have just one link if user selected by title
    tagged_dictionary = remove_closedclasscategories(get_tagged_from_json())
    # save the new article
    with open('Results/pos_tags_noclosed.json', 'w')as json_out:
        json.dump(tagged_dictionary, json_out)
    lemmas = get_lemmas(tagged_dictionary)

    print('Counting lemma appearances')
    # count frequencies and construct inverted index
    with open('Results/inverted_index.xml', 'w') as vct:
        root = ET.Element("inverted_index")
        for lemma in lemmas:
            lemma_name = ET.SubElement(root, "lemma", name=lemma)
            # lemma_weights = []
            for key in tagged_dictionary:

                count_in_article = 0
                tf = term_frequency(lemma, tagged_dictionary[key])
                idf = inverse_document_frequency(lemma, tagged_dictionary)
                lemma_weight = tf * idf
                # lemma_weights.append([key, lemma_weight])

                document = ET.SubElement(lemma_name, "document", id=key, weight=str(lemma_weight))
            tree = ET.ElementTree(root)
            tree.write('Results/inverted_index.xml')
            # json.dump({f'{lemma}': f"{json.dumps(lemma_weights)}"}, vct)
    print('Successfully created index. It can be found in the Results folder')


def get_tagged_from_json():
    # gets the tagged articles from local files
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
    # stem and lemmatize
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer('english')
    lemmas = []
    for key in tagged_dictionary:
        for pair in tagged_dictionary[key]:
            if len(pair) == 0:
               continue
            else:
                if lemmatizer.lemmatize(pair[0]) not in lemmas:
                    lemmas.append(stemmer.stem(lemmatizer.lemmatize(pair[0], pos=get_wordnet_pos(pair[1]))))

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


def term_frequency(term, doc):
    term_count = 0.00
    word_count = 0.01
    # count term frequency in d
    for pair in doc:
        if len(doc) == 0:
            continue
        else:
            if len(pair) == 0:
                continue
            else:
                if term in pair[0]:
                    term_count += 1
                word_count += 1

    return term_count/word_count


def inverse_document_frequency(term, doc):
    # calcilates idf given a term and a documents
    times_in_documents = 0.01
    for key in doc:
        for pair in doc[key]:
            if len(pair) == 0:
                continue
            else:
                if term in pair[0]:
                    times_in_documents += 1

    metric = len(doc)/times_in_documents
    return math.log(metric, 10)
