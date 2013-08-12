import model
import redis
from lexicon import lexicon_names, lexicon_setup
from data_processing import build_dish_corpus


def persist_lexicon_lists(lexicon):
# put into redis
	pass

def initialize_categories(lexicon):
# for each category name, make an empty list in redis
	pass	


def id_category(dish, corpus):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup?
    # for dish, tokens in corpus.items():
    dish_categories = []
    #     for word in tokens:
            # for lexicon in lexicon_lists:
    #         if [word in lexicon]
                dish_categories.append(word)
    return dish_categories


def categories_for_corpus(corpus):
# call classification function for all dishes in corpus
    dishes_to_categories = {}
    categories_to_dishes = {}
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for dish in corpus.keys():
        categories = id_category(dish)
        for category in categories:
            # add category tags to dish, persist to redis
                dish_key = ('item_categories:' + str(dish.id))
                r.lpush(dish_key, category)
            # add dish_id to category list, persist to redis
                category_key = ('category_items:' + str(dish.id))
                r.lpush(category_key, dish.id)
            r.save



# old functions below -- for reference

def categories_for_corpus(corpus):
    dishes_to_categories = {}
    for dish_id, text in corpus.items():
        category = id_category(dish_id, corpus)
        dishes_to_categories[dish_id] = category
    return dishes_to_categories


def map_categories_to_dishes(dishes_to_categories):
    categories_to_dishes = {}
    for dish_id, categories in dishes_to_categories.items():
        for c in categories:
            categories_to_dishes.setdefault(c, [])
            categories_to_dishes[c].append(dish_id)
    return categories_to_dishes


def persist_categories(categories_to_dishes):
    category_id = 1
    for category, dishes in categories_to_dishes.items():
        new_category = model.Category(name=category, id=category_id)
        model.session.add(new_category)
        for dish in dishes:
            item = model.session.query(model.Item).get(dish)
            item.category = category_id
            model.session.add(item)
        model.session.commit()
        category_id += 1


def find_category_frequencies(categories_to_dishes):
    category_freq = {}
    for category, dishes in categories_to_dishes.items():
        category_freq[category] = len(dishes)
    return category_freq


def sort_category_frequencies(category_freq):
    sorted_category_freq = []
    for category, frequency in category_freq.items():
        sorted_category_freq.append((frequency, category))
    return sorted_category_freq
