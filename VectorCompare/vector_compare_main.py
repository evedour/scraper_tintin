from sklearn.datasets import fetch_20newsgroups
import compare
import preprocessor
import json
import gensim
import weights
from gensim import corpora
from gensim.utils import simple_preprocess
from scipy import spatial
from Scraper.NewsScrape import indexer
from bs4 import BeautifulSoup

print(f'\n########Σύστημα σύγκρισης συλλογών########\n')
print(f'####Project Γλωσσικής Τεχνολογίας - Σεπτέμβρης 2021####\n')
print('##########################################################')


def main():
    collection_e = fetch_20newsgroups(subset='train')
    collection_a = fetch_20newsgroups(subset='test')

    user_in = input('Run preprocessor? Y/N: ')
    if user_in.upper() == 'Y':
        # tokenize and lemmatize all documents in collection E
        print('Extracting lemmas in collection E: \n')
        e_processed = preprocessor.exctract_themes(collection_e.data[:1000], 'e')
        print('\nExtracting lemmas in collection A: \n')
        a_processed = preprocessor.exctract_themes(collection_a.data[:1000], 'a')

        # create dictionary based on the created lemmas
        # dictionary.token2id has id for tokens
        e_dictionary = gensim.corpora.Dictionary(e_processed)
        a_dictionary = gensim.corpora.Dictionary(a_processed)
        e_dictionary.save('Data/e_dictionary.txtdic')
        a_dictionary.save('Data/a_dictionary.txtdic')
        # create a dictionary reporting appearances of each word in each doc of collection e
        # this holds the number of appearances for each word in dictionary
        e_cor = [e_dictionary.doc2bow(doc) for doc in e_processed]
        a_cor = [a_dictionary.doc2bow(doc) for doc in a_processed]

        e_index = indexer.make_index(e_dictionary, e_cor, range(len(e_cor)), name='e')
        a_index = indexer.make_index(a_dictionary, a_cor, range(len(a_cor)), name='a')

    e_dictionary =corpora.Dictionary.load('Data/e_dictionary.txtdic')
    a_dictionary =corpora.Dictionary.load('Data/a_dictionary.txtdic')
    themes_dictionary = {k: v for k, v in sorted(e_dictionary.dfs.items(), key=lambda item: item[1])}

    e_weights = weights.get_weights('inverted_index_e.xml', collection_e, themes_dictionary, e_dictionary)
    a_weights = weights.get_weights('inverted_index_a.xml', collection_a, themes_dictionary, a_dictionary)

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

main()
