import json

def vectorize(links):
    # links is a list of links, that can have just one link if user selected by title
    tagged_dict = get_tagged_from_json()
    tagged_dictionary = remove_closedclasscategories(tagged_dict)
    with open('Results/pos_tags_noclosed.json', 'w')as json_out:
        json.dump(tagged_dictionary, json_out)
        json_out.close


def get_tagged_from_json():
    with open('Results/pos_tags.json') as jsonfile:
        tagged_dict = json.load(jsonfile)
    return tagged_dict


def remove_closedclasscategories(tagged_dic):
    closedclasscategories = ['.', ',', ':', 'CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', ".", ",", ":", "D" "C" "T" "X" "N" "S" "D" "DT" "OS" "RP" "RP$" "P" "O" "H" "DT" "P" "P$" "RB"]
    for key in tagged_dic:
        article = tagged_dic[key]
        for pair in article:
            if pair[1] in closedclasscategories:
                pair.clear()
        tagged_dic[key] = article
    return tagged_dic
