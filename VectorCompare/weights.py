import math
import xml.etree.cElementTree as ET
import json
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def get_tfidf(cor, dictionary, name):
    with open(f'Data/collection_{name}.xml', 'w') as Exml:
        root = ET.Element(f'{name}_vector')
        weights_vector = []
        for text in cor:
            # text is list of tuples (lemma_id, appearances in article)
            weights = []
            article_id = ET.SubElement(root, 'article', id=str(cor.index(text)))
            for id in range(len(dictionary.token2id)):
                # id is the id of the lemma
               for lemma, appearances in text:
                   tf = 0
                   if id == lemma:
                       tf = appearances/len(text)
               for key in dictionary:
                   if key == id:
                       idf = len(cor) / dictionary.dfs[key]
               tfidf = float(tf*idf)

               for key in dictionary.token2id:
                   if dictionary.token2id[key] == id:
                       nme = key

               term = ET.SubElement(article_id, 'term', name=nme, weight=str(tfidf))
               weights.append((id, str(tfidf)))
            weights_vector.append(weights)
            tree = ET.ElementTree(root)
            tree.write(f'Data/collection_{name}.xml')

    return weights_vector