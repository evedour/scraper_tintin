from scipy import spatial
from operator import itemgetter


def compare_by_cosine(vector, article):
    res = spatial.distance.cosine(vector, article)
    return res


def compare_by_jaccard(vector, article):
    res = spatial.distance.jaccard(vector, article)
    return res


def compare(vector, collection):
    result_cosine = []
    result_jaccard = []
    vec_in = [float(item) for t in vector for item in t]

    for article in collection:
        index = collection.index(article)
        art_in = [float(item) for t in article for item in t]
        if len(vec_in) > len(art_in):
            max_idx = len(art_in)
            del vec_in[max_idx:]
        elif len(art_in) > len(vec_in):
            max_idx = len(vec_in)
            del art_in[max_idx:]
        result_cosine.append([compare_by_cosine(vec_in, art_in), index])
        result_jaccard.append([compare_by_jaccard(vec_in, art_in), index])

    result_cosine.sort(key=itemgetter(0))
    result_jaccard.sort(key=itemgetter(0))

    return result_cosine, result_jaccard
