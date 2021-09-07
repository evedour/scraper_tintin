from bs4 import BeautifulSoup


def query(words):
    soup = BeautifulSoup(open('./Results/inverted_index.xml', 'r'), 'lxml')
    for word in words:
        lemma = soup.findAll('lemma', {"name": f"{word.lower()}"})
        if len(lemma) == 0:
            print(f'{word} not found in lemmas')
            continue
        else:
            weights = []
            ids = []
            for document in lemma[0].find_all('document'):
                if float(document.attrs['weight'])> 0.0:
                    weights.append(document.attrs['weight'])
                    ids.append(document.attrs['id'])

            zipped = zip(weights, ids)
            sorted_pairs = sorted(zipped)
            tuples = zip(*sorted_pairs)
            weights, ids = [list(tuple) for tuple in tuples]
            print(f'Results for lemma {word}: \n')
            for id in ids:
                print(f'{id}\n')
