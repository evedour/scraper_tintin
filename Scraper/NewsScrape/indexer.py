import math
import xml.etree.cElementTree as ET
import json
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def make_index(dictionary, cor, links):
    # count frequencies and construct inverted index
    with open('Results/inverted_index.xml', 'w') as index_out:
        print('Making xml file for inverted index')
        root = ET.Element("inverted_index")
        for lemma in list(lemmas for lemmas in dictionary.token2id):
            lemma_name = ET.SubElement(root, "lemma", name=lemma)
            lemma_id = dictionary.token2id[lemma]
            for key in cor:
                doc_id = cor.index(key)
                for pair in key:
                    if pair[0] == lemma_id:
                        tf = pair[0] / len(key)
                        break
                idf = dictionary.num_docs / dictionary.dfs[lemma_id]
                lemma_weight = tf * idf
                document = ET.SubElement(lemma_name, "document", id=key, weight=str(lemma_weight))

            tree = ET.ElementTree(root)
            tree.write('Results/inverted_index.xml')
    print('Successfully created index. It can be found in the Results folder')
