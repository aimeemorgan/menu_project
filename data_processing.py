import model
import nltk
from lexicon import lexicon_names, lexicon_setup
from datetime import datetime 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# preprocessing

def build_dish_corpus():
# build a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation.
    dish_list = model.session.query(model.Item).all()
    dish_corpus = {}
    for dish in dish_list:
        text = (dish.description).lower().strip().strip('*')
        tokens = nltk.word_tokenize(text)
        dish_corpus[dish.id] = tokens
    return dish_corpus


def build_menu_corpus():  # what am I actually planning to use this for?
# build a dictionary where key is menu.id, value is tokenized list
# with text of item.descriptions for all items that appear on menu.
# lowercase/strip punctuation
    menu_list = model.session.query(model.Menu).all()
    menu_corpus = {}
    for menu in menu_list:
        for item in menu.items:
            if item.item:
                text = (item.item.description).lower().strip() + '. '
                tokens = nltk.word_tokenize(text)
        menu_corpus[menu.id] = tokens
    return menu_corpus


def strip_prepositional_phrases(corpus):
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    for id, tokens in corpus:
        for i in len(tokens):
            if tokens[i] in ['of', 'from', 'in', 'with', 'accompanied']:
                tokens = tokens[0:(i-1)]


def strip_stopwords():
# take a corpus, remove stopwords from nltk stopword set
    pass


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


def classify_dishes(dish_corpus):
# classify dishes
# likely to be function that calls a bunch of subfunctions for various
# classification tasks
    pass


def find_similar_dishes(dish):
# for a given dish, use fuzzy search to find the (10?) most similar
# dishes. return a list of dish IDs in descending order of similarity
    pass


def similar_dishes_for_corpus(corpus):
# For a given corpus, return a dictionary with each dish ID mapped to a list of dish IDs
# of similar dishes, ordered in descending order of similarity.
# (if this runs too slowly: refactor so that results get pushed to database as calculated
# for each dish -- will need to add check to see if similar dishes have already been calculated
# for each dish)
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

# def techniques_for_corpus(corpus):
# should return a dictionary that maps menu items to list of techniques]
#     technique_mappings = {}
#     for id, text in corpus.items():
#       call find techniques
            # for each technique in list that gets returned:
            #     check for technique in technique_mappings
            #         if not there: add as key w/ value = 
            #         list containing item id of dish
            #         if there: append dish ID to end of value list


def map_techniques_to_dishes(techniques):
# using dictionary from previous function, generate a count of
# how often each technique appears. return a dictionary of
# technique names mapped to dish IDs.
    pass


def find_technique_frequencies(technique_dict):
# using result from previous function, generate a list of
# techniques with a count of how often they appear in the dataset,
# ordered from highest to lowest frequency.
    pass


def id_category(dish):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup? attempt to implement w/ supervised classification -- go through subset
# of dish descriptions, create a training set?
    pass


def categories_for_corpus(corpus):
    pass


def map_categories_to_dishes(corpus):
    pass


def find_category_frequencies():
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

if __name__=="__main__":
    corpus = build_dish_corpus()
    lexicon = lexicon_setup()