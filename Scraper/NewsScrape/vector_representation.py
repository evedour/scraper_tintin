import json

def vectorize(links):
    # links is a list of links, that can have just one link if user selected by title
    get_tagged_from_json()


def get_tagged_from_json():
    with open('Results/pos_tags.json') as jsonfile:
        tagged_dict = json.load(jsonfile)
