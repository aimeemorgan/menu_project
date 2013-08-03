import model
import nltk
from nltk.corpus import stopwords
from lexicon import lexicon_names, lexicon_setup
from datetime import datetime 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# preprocessing

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


def strip_prepositional_phrases(corpus):
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    for id, tokens in corpus.items():
        for i in range(len(tokens)):
            if tokens[i] in ['of', 'from', 'in', 'with', 'accompanied']:
                tokens = tokens[0:(i-1)]


def strip_stopwords(corpus):
# take a corpus, remove stopwords from nltk stopword set
    stoplist = stopwords.words('english')
    for dish, words in corpus.items():
        for word in words:
            if word in stoplist:
                del word
        corpus[dish] = words
    return corpus


# classification

def word_frequencies(corpus):
# build a dictionary with corpus words mapped to the number
# of timtes they appear.
    frequencies = {}
    for dish, words in corpus.items():
        for word in words:
            frequencies.setdefault(word, 0)
            frequencies[word] += 1
    return frequencies


def most_frequent_sorted(frequencies):
    ranked_freq = []
    for word, count in frequencies.items():
        ranked_freq.append((count, word))
    return sorted(ranked_freq)


def find_similarity_scores(item_id, dish_corpus):
# for a given dish, use fuzzy search to calculate similarity scores
# for other dishes in the corpus. return a list of dish IDs in descending order of 
# similarity
    scores = {}
    comparison_desc = dish_corpus[item_id]
    for item, desc in dish_corpus.items():
        if item_id != item:
            score = fuzz.token_set_ratio(dish_corpus[comparision_desc], desc)
            scores[item] = score
    return scores


def rank_similarities(scores):
    ranked_scores = []
    while len(ranked_scores) < 10:
        for item, score in scores.items():
            ranked_scores.append((score, item))
    return sorted(ranked_scores)


def similar_dishes_for_corpus(dish_corpus):
# Return a dictionary with each dish ID from corpus mapped to a list of dish IDs
# of 10 similar dishes, ordered in descending order of similarity.
    similarities = {}
    for dish_id, text in dish_corpus.items():
        scores = find_similarity_scores(dish_id)
        similar_list = rank_similarities(scores)
        similarities[dish_id] = similar_list
    return similarities
# (if this runs too slowly: refactor so that results get pushed to database as calculated
# for each dish -- will need to add check to see if similar dishes have already been calculated
# for each dish)

# def persist_similarities(similarities):
#     for dish_id, dishes in similarities:
#         for dish in dishes:
#             new_similarity = 


def dishes_that_appear_with(dish):
# For a given dish, generate a list of IDs of dishes that frequently
# appear on the same menu as that dish.
    pass


def id_techniques(dish):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods.
    dish_words = corpus[dish]
    techniques = []
    for word in dish_words:
        suffix = str(word[-2:])
        if suffix == 'ed':
            techniques.append(word)
    if len(techniques) > 0:
        return techniques
    else:
        return None


def techniques_for_corpus(corpus):
    dishes_to_techniques = {}
    for dish_id, text in corpus.items():
        techniques = id_category(dish_id)
        dishes_to_categories[dish_id] = techniques
    return dishes_to_techniques


def map_techniques_to_dishes(dishes_to_techniques):
    techniques_to_dishes = {}
    for dish_id, techniques in dishes_to_techniques.items():
        for c in techniques:
            techniques_to_dishes.setdefault(c, [])
            techniques_to_dishes[c].append(dish_id)
    return techniques_to_dishes


# def persist_techniques(techniques_to_dishes):
# # write technique info to Techniques table.
#     technique_id = 1
#     for technique, dishes in techniques_to_dishes.items():
#         new_technique = model.Technique(name=technique, id=technique_id)
#         session.add(new_technique)
#         for dish in dishes:
#             !!!!!new_itemtechnique = model.Technique(name=technique, id=technique_id)
#         session.commit()
#         technique_id += 1


def persist_techniques_to_dishes(techniques_to_dishes):
# write new ItemTechnique relationship to database
    pass



def find_technique_frequencies(techniques_to_dishes):
    technique_freq = {}
    for technique, dishes in techniques_to_dishes.items():
        technique_freq[technique] = len(dishes)
    return technique_freq


def sort_technique_frequencies(technique_freq):
    sorted_technique_freq = []
    for technique, frequency in technique_freq.items():
        sorted_technique_freq.append((frequency, technique))
    return sorted_technique_freq


def id_category(dish):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup? attempt to implement w/ supervised classification -- go through subset
# of dish descriptions, create a training set?
    pass


def categories_for_corpus(corpus):
    dishes_to_categories = {}
    for dish_id, text in corpus.items():
        category = id_category(dish_id)
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


def find_similar_restaurant(restaurant):
# find restaurants similar to input restaurant based on comparison of dishes
# this should be precalculated, persisted -- move to data processing?
    pass

###########################################
# postprocessing

# some kind of master function for reading classification info
# from dictionaries, writing to csv files for import to database for webapp
# (likely to be called from within classification subfunctions)


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

# if __name__=="__main__":
#     corpus = build_dish_corpus()
#     lexicon = lexicon_setup()