import model
from nltk.stem import PorterStemmer
from lexicon import lexicon_names
from data_processing import build_dish_corpus


def lexicon_setup():
    stemmer = PorterStemmer()
    lexicon_lists = {}
    for name in lexicon_names:
        filepath = './lexicon/' + name + '.txt'
        f = open(filepath)
        lexicon_lists.setdefault(name, {})
        for row in f:
            new_entry = row.strip().lower()
            term = stemmer.stem(new_entry)
            lexicon_lists[name][term] = 1
    return lexicon_lists


def id_category(dish, corpus, lexicon_lists):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup?
    print dish
    stemmer = PorterStemmer()
    tokens = corpus[dish]
    categories = []
    for word in tokens:
        word = stemmer.stem(word)
        for category, lexicon in lexicon_lists.items():
            if word in lexicon:
                if category not in categories:
                    categories.append(category)
    return categories


def categories_for_corpus(corpus, lexicon_lists):
# call classification function for all dishes in corpus
    for dish in corpus.keys():
        categories = id_category(dish, corpus, lexicon_lists)
        print categories
        for category in categories:
                # add category tags to dish, persist to redis
                dish_key = ('item_categories:' + str(dish))
                model.r.lpush(dish_key, category)
                # add dish_id to category list, persist to redis
                category_key = ('category_items:' + str(category))
                model.r.lpush(category_key, dish)
                model.r.save
                print "SUCCESS"

