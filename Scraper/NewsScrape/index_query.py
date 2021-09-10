from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer, SnowballStemmer


def query(words):
    # read index
    soup = BeautifulSoup(open('./Results/inverted_index.xml', 'r'), 'lxml')
    with open('Results/lemmas.txt', 'r')as lemmas_in:
        lemmas = [line.split(',') for line in lemmas_in.readlines()]

    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer()

    wghts = []
    links = []

    for wrd in words:
        #lemmatize query
        word = stemmer.stem(lemmatizer.lemmatize(wrd, 'v'))
        for lem in lemmas:
            if word in lem:
                word = lem
                break

        lemma = soup.findAll('lemma', {"name": f"{word.lower()}"})
        # find query in lemmas and return the result based on tf-idf weight
        if len(lemma) == 0:
            print(f'No matches found for {word} ')
            continue
        else:

            for document in lemma[0].find_all('document'):
                if float(document.attrs['weight'])> 0.0:
                    wghts.append(document.attrs['weight'])
                    links.append(document.attrs['id'])
    if len(links) > 0:
        zipped = zip(wghts, links)
        sorted_pairs = sorted(zipped)
        tuples = zip(*sorted_pairs)
        wghts, links = [list(tuple) for tuple in tuples]
        for id in links:
            for is_same in links:
                if is_same == id:
                    wghts[links.index(id)] += wghts[links.index(is_same)]
                    links.remove(is_same)

        print(f'Results: \n')
        count = 0
        for id in links:
            count += 1
            print(f'{id}\n')
        print(f'Query returned {count} results')
