import model
import nltk
import redis
from nltk.corpus import stopwords
#from lexicon import lexicon_names, lexicon_setup
from datetime import datetime 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# preprocessing

def build_itemid_index():
    item_list = model.session.query(model.Item).all()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for item in item_list:
        r.lpush('itemid_index', item.id)
    r.save


def build_dish_corpus():
# builds a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation.
    dish_list = model.session.query(model.Item).all()
    dish_corpus = {}
    for dish in dish_list:
        text = (dish.description).lower().strip().strip('*')
        tokens = nltk.word_tokenize(text)
        dish_corpus[dish.id] = tokens
    return dish_corpus


def build_dish_corpus_no_tokens():
# for fuzzy search
    dish_list = model.session.query(model.Item).all()
    dish_corpus = {}
    for dish in dish_list:
        text = (dish.description).lower().strip().strip('*')
        dish_corpus[dish.id] = text
    return dish_corpus


def build_menu_corpus():  # what am I actually planning to use this for?
# ngrams? collocations?
# builds a dictionary where key is menu.id, value is tokenized list
# with text of item.descriptions for all items that appear on menu.
# lowercase/strip punctuation
    menu_list = model.session.query(model.Menu).all()
    menu_corpus = {}
    for menu in menu_list:
        tokens = []
        for item in menu.items:
            if item.item:
                text = (item.item.description).lower().strip() + '. '
                new_tokens = nltk.word_tokenize(text)
                tokens.append(new_tokens)
        menu_corpus[menu.id] = tokens
    return menu_corpus


def persist_corpus(name, corpus):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for item_id, tokens in corpus.items():
        for token in tokens:
            key = (name +':%s') % item_id
            r.lpush(key, token)
    r.save


def load_corpus(item_index_name, corpus_prefix):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    index = r.lrange(item_index_name, 0, -1)
    corpus = {}
    for item in index:
        key =  corpus_prefix + ':%s' % item
        values = r.lrange(key, 0, -1)
        corpus[int(item)] = values
    return corpus


def strip_prepositional_phrases(corpus):
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    for id, tokens in corpus.items():
        for i in range(len(tokens)):
            if tokens[i] in ['of', 'from', 'in', 'with', 'accompanied']:
                tokens = tokens[0:(i-1)]
    return corpus
# not working -- why? index error


def strip_stopwords(corpus):
# take a corpus, remove stopwords from nltk stopword set
    stoplist = stopwords.words('english')
    print stoplist
    for entry in stoplist:
        entry = entry.encode('utf-8')
    corpus = dict(corpus)
    for dish, description in corpus.items():
        for word in description:
            if word in stoplist:
                description.remove(word)
        corpus[dish] = description
    return corpus



# classification

def word_frequencies(corpus):
# build a dictionary with corpus words mapped to the number
# of times they appear.
    frequencies = {}
    for dish, words in corpus.items():
        for word in words:
            frequencies.setdefault(word, 0)
            frequencies[word] += 1
    return frequencies


def build_word_index(freq):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for word in freq.keys():
        r.lpush('word_index', word)
    r.save


def persist_word_frequencies(frequencies):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)    
    for word, freq in frequencies.items():
            key = ('frequency:%s') % word
            r.lpush(key, freq)
    r.save


def load_word_frequencies():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)  
    index = r.lrange('word_index', 0, -1)
    freq = {}
    for word in index:
        key =  'frequency:%s' % word
        value = r.lrange(key, 0, -1)
        freq[word] = value
    return freq


def most_frequent_sorted(frequencies):
    ranked_freq = []
    for word, count in frequencies.items():
        ranked_freq.append((count, word))
    return sorted(ranked_freq)


# def find_similarity_scores(item_id, dish_corpus):
# # for a given dish, use fuzzy search to calculate similarity scores
# # for other dishes in the corpus. 
#     scores = {}
#     comparison_desc = dish_corpus[item_id]
#     for item, desc in dish_corpus.items():
#         if item_id != item:
#             score = fuzz.token_set_ratio(comparison_desc, desc)
#             if score >= 90:
#                 scores[item] = score
#     return scores


# def rank_similarities(scores):
#     ranked_scores = []
#     for item, score in scores.items():
#         ranked_scores.append((score, item))
#     ranked_scores = sorted(ranked_scores, reverse=True)
#     top_25 = ranked_scores[0:25]
#     print top_25
#     return top_25


# def similar_dishes_for_corpus(dish_corpus):
# Return a dictionary with each dish ID from corpus mapped to a list of dish IDs
# of 25 similar dishes, ordered in descending order of similarity.
# refactor so that dishes are removed from the corpus as they are matched
    # similarities = {}
    # for dish_id in dish_corpus.keys():
    #     scores = find_similarity_scores(dish_id, dish_corpus)
    #     top_25 = rank_similarities(scores)    
    #     similarities[dish_id] = top_25
    # return similarities

# refactor to persist in redis
# def persist_similarities(similarities):
#     for dish_id, ranked_scores in similarities:
#         similarity_id = 0
#         for item in ranked_scores:
#             new_similarity = new_itemsimilarity = model.ItemSimilarity(
#                                                     id = similarity_id,
#                                                     item_id_1 = dish_id,
#                                                     item_id_2 = item[1],
#                                                     score = item[0])
#             session.add(new_similarity)
#             session.commit()




def dishes_that_appear_with(dish):
# For a given dish, generate a list of IDs of dishes that frequently
# appear on the same menu as that dish.
# so basically, for a given dish ID:
# 1. get all menus on which that dish appears (there's a function!)
# 1.5 count all menus on which that dish appears, save count
# 2. make a blank dictionary
# 3. for each menu, add each item on the menu to the blank dictionary w count of occurences
# 4. for each entry in dictionary: replace value with value/menu count to get ratio
#    (between 0 and 1)
# 5: make list mapping frequency ratio to dish ID
    pass
    

def appears_with_for_corpus(corpus):
# call above fucntion for every dish in corpus
    appearances = {}
    for dish_id, description in corpus.items():
        appearances [dish_id] = dishes_that_appear_with(dish_id)
    return appearances


def id_techniques(dish_id, corpus):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods.
    dish_words = corpus[dish_id]
    techniques = []
    for word in dish_words:
        if len(word) > 2:
            suffix = (word[-2:]).encode('utf-8')
            if suffix == 'ed':
                techniques.append(word)
    if len(techniques) > 0:
        return techniques
    else:
        return "unknown"


def techniques_for_corpus(corpus):
    dishes_to_techniques = {}
    for dish_id, text in corpus.items():
        techniques = id_techniques(dish_id, corpus)
        if techniques:
            dishes_to_techniques[dish_id] = techniques
    return dishes_to_techniques


def map_techniques_to_dishes(dishes_to_techniques):
    techniques_to_dishes = {}
    false_matches = {'bed': 0, 'red': 0, 'served': 0, 'assorted': 0}
    for dish_id, techniques in dishes_to_techniques.items():
        for c in techniques:
            if c not in false_matches:
                if len(c) > 1:
                    techniques_to_dishes.setdefault(c, [])
                    techniques_to_dishes[c].append(dish_id)
    return techniques_to_dishes


def persist_techniques(techniques_to_dishes):
# write technique info to Techniques table.
    technique_id = 1
    itemtechnique_id = 1
    for technique, dishes in techniques_to_dishes.items():
        new_technique = model.Technique(name=technique, id=technique_id)
        model.session.add(new_technique)
        for dish in dishes:
            new_itemtechnique = model.ItemTechnique(item_id=dish, 
                                                    technique_id=technique_id)
            model.session.add(new_itemtechnique)
            model.session.commit()
            itemtechnique_id += 1
        technique_id += 1


def find_technique_frequencies(techniques_to_dishes):
    technique_freq = {}
    for technique, dishes in techniques_to_dishes.items():
        technique_freq[technique] = len(dishes)
    return technique_freq


def sort_technique_frequencies(technique_freq):
    sorted_technique_freq = []
    for technique, frequency in technique_freq.items():
        sorted_technique_freq.append((frequency, technique))
        sorted_technique_freq = sorted(sorted_technique_freq)
    return sorted_technique_freq


# def id_category(dish, corpus):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup? attempt to implement w/ supervised classification -- go through subset
# of dish descriptions, create a training set?
    # for dish, tokens in corpus.items():
    #     for word in tokens:
    #         if [word in lexicon]
          # for word in tokens:



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
        new_cateogory = model.Category(name=category, id=category_id)
        session.add(new_category)
        for dish in dishes:
            item = model.session.query(model.Item).get(num)
            item.category = category_id
            session.add(item)
        session.commit()
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



###########################################
# postprocessing

# some kind of master function for reading classification info
# from dictionaries, writing to csv files for import to database for webapp
# (likely to be called from within classification subfunctions)
# try it using above functions first - -see how slow it is.


###########################################


# helper functions

def find_unclassified(category):
# find dishes that lack a classification term for a given
# category (to aid in refinement of classification)
    pass


# functions to not build unless lots of extra time


# def id_fancy_foods(dish):
#     pass


# def id_venue(restaurant):
# # identify "restaurants" that are actually ships, railroad cars, etc.
# # look for "on board", "en route", "S.S.", etc.
#     pass

# def id_main_ingredient(dish):
# # identfy main ingredient of a dish
# # look for nouns; prep phrases will have been stripped
# # if more than 1 noun: noun in list of meats/proteins most likely main
# # main ingredient?
#     pass


# def ingredients_for_corpus(corpus):
#     pass


# def map_ingredients_to_dishes():
#     pass


# def find_ingredient_frequencies():
#     pass

# def find_similar_restaurant(restaurant):
## find restaurants similar to input restaurant based on comparison of dishes
# # this should be precalculated, persisted -- move to data processing?
# 1. get menu list for restaurant
# 2. for other 


# if __name__=="__main__":
#     corpus = build_dish_corpus()
#     # lexicon = lexicon_setup()