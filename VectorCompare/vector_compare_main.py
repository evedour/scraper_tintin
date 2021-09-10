from sklearn.datasets import fetch_20newsgroups
import compare
import preprocessor
import weights
import json
import gensim
from gensim.utils import simple_preprocess
from scipy import spatial


def main():
    collection_e = fetch_20newsgroups(subset='train')
    collection_a = fetch_20newsgroups(subset='test')

    user_in = input('Run preprocessor? Y/N: ')
    if user_in.upper() == 'Y':
        idx = 100
        e_processed = []
        a_processed = []
        for doc in collection_e.data[:idx]:
            # tokenize and lemmatize all documents in collection E
            e_processed.append(preprocessor.exctract_themes(doc, 'e'))
        for doc in collection_a.data[:idx]:
            a_processed.append(preprocessor.exctract_themes(doc, 'a'))
        # create dictionary based on the created lemmas
        # dictionary.token2id has id for tokens
        e_dictionary = gensim.corpora.Dictionary(e_processed)
        a_dictionary = gensim.corpora.Dictionary(a_processed)
        # create a dictionary reporting appearances of each word in each doc of collection e
        # this holds the number of appearances for each word in dicionary
        e_cor = [e_dictionary.doc2bow(doc) for doc in e_processed]
        a_cor = [a_dictionary.doc2bow(doc) for doc in a_processed]

        e_weights = weights.get_tfidf(e_cor, e_dictionary, 'e')
        a_weights = weights.get_tfidf(a_cor, a_dictionary, 'a')

        with open('Data/e_weights.json', 'w')as e_out:
            json.dump(e_weights, e_out)
            e_out.close()
        with open('Data/a_weights.json', 'w')as a_out:
            json.dump(a_weights, a_out)
            a_out.close()

    with open('Data/e_weights.json', 'r')as e_in:
        e_weights = [[tuple(x) for x in list] for list in json.load(e_in)]
        e_in.close()
    with open('Data/e_weights.json', 'r')as a_in:
        a_weights = [[tuple(x) for x in list] for list in json.load(a_in)]
        a_in.close()

    flag = True
    while flag:
        print('Type \"STOP\" to quit the program')
        user_in = input(f'Type an article id between 0 and {len(a_weights)} to check similarities with E collection: ')
        if user_in.upper() == 'STOP':
            flag = False
            break
        result_cosine, result_jaccard = compare.compare(a_weights[int(user_in)], e_weights)
        print('-------------------------------------------------------------------------')
        print('Top three most similar articles: \n')
        for i in range(3):
            print(f'{collection_e.data[i][:100]}\n')
            print('############################################################################')
        idx_a = collection_a.target[int(user_in)]
        print(f'Article number {user_in} has been categorized as {collection_a.target_names[idx_a]}\n')

        print('Checking if my cosine results where correct....')
        print('The top three results where categorized as: ')
        for i in range(3):
            print(f'Article number {i} has been categorized as {collection_e.target_names[collection_e.target[result_cosine[i][1]]]}\n')

        print('Checking if my Jaccard results where correct....')
        print('The top three results where categorized as: ')
        for i in range(3):
            print(f'Article number {i} has been categorized as {collection_e.target_names[collection_e.target[result_jaccard[i][1]]]}\n')

    print('')
