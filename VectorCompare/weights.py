from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import json
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def get_weights(filename, collection, dictionary, dic):
    themes_id = [lemma_id for lemma_id in dictionary]
    themes_keys = list(dic.token2id.keys())
    themes_values = list(dic.token2id.values())
    weights_vector = []
    with open(filename) as e_xml:
        soup = BeautifulSoup(e_xml, 'xml')
        for doc in range(len(collection.data[:1000])):
            weights = []
            for id in themes_id[:100]:
                if id in dic.token2id.values():
                    lemma = soup.findAll('lemma', {"name": f"{themes_keys[id]}"})
                    document = lemma[0].findAll('document', {"id": f'{doc}'})
                    attributes = dict(document[0].attrs)
                    if float(attributes['weight']) > 0.0:
                        weights.append((id, float(attributes['weight'])))
            weights_vector.append(weights)

    return weights_vector