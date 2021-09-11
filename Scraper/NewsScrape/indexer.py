import math
import xml.etree.cElementTree as ET
import json
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from progressbar import ProgressBar


def make_index(dictionary, cor, links, name=""):
    pbar = ProgressBar()
    # count frequencies and construct inverted index
    if name == "":
        filename = 'Results/inverted_index.xml'
    else:
        filename = f'inverted_index_{name}.xml'
    with open(filename, 'w') as index_out:
        print('Making xml file for inverted index')
        root = ET.Element("inverted_index")
        lemma_list = list(dictionary.token2id.keys())
        lemma_id_list = list(dictionary.token2id.values())
        for lemma_id in pbar(range(len(dictionary.token2id))):
            idx = lemma_id_list.index(lemma_id)
            lemma_n = lemma_list[idx]
            lemma_name = ET.SubElement(root, "lemma", name=str(lemma_n))
            i = 0

            for key in cor:
                doc_id=links[i]
                i += 1
                r = [item for item in key if item[0] == lemma_id]
                if len(r) == 0:
                    tf = 0
                else:
                    tf = r[0][0] / len(key)
                idf = dictionary.num_docs / dictionary.dfs[lemma_id]
                lemma_weight = tf * idf
                document = ET.SubElement(lemma_name, "document", id=str(doc_id), weight=str(lemma_weight))

        tree = ET.ElementTree(root)
        tree.write(filename)

    print('Successfully created index. It can be found in the Results folder')
