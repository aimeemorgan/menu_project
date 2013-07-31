import model
import nltk
from lexicon import lexicon_names, lexicon_setup
from datetime import datetime 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# preprocessing

def build_dish_corpora():
# build a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation.
    dish_list = model.session.query(model.Item).all()
    dish_corpora = {}
    for dish in dish_list:
        text = (dish.description).lower().strip().strip('*')
        tokens = nltk.word_tokenize(text)
        dish_corpora[dish.id] = tokens
    return dish_corpora


def build_menu_corpora():
# build a dictionary where key is menu.id, value is tokenized list
# with text of item.descriptions for all items that appear on menu.
# lowercase/strip punctuation
    menu_list = model.session.query(model.Menu).all()
    menu_corpora = {}
    for menu in menu_list:
        for item in menu.items:
            if item.item:
                text = (item.item.description).lower().strip() + '. '
                tokens = nltk.word_tokenize(text)
        menu_corpora[menu.id] = tokens
    return menu_corpora


def strip_prepositional_phrases(corpora):
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    for id, tokens in corpora:
        for i in len(tokens):
            if tokens[i] in ['of', 'from', 'in', 'with', 'accompanied']:
                tokens = tokens[0:(i-1)]


def strip_stopwords():
# take a corpora, remove stopwords from nltk stopword set
    pass


# classification

def word_frequencies(corpora):
# build a dictionary with corpora words mapped to the number
# of timtes they appear.
    frequencies = {}
    for dish, words in corpora.items():
        for word in words:
            frequencies.setdefault(word, 0)
            frequencies[word] += 1
    return frequencies


def most_frequent_sorted(frequencies):
    ranked_freq = []
    for word, count in frequencies.items():
        ranked_freq.append((count, word))
    return sorted(ranked_freq)


def classify_dishes(corpora):
# classify dishes
# likely to be function that calls a bunch of subfunctions for various
# classification tasks
    pass


def cluster_dishes(corpora):
# cluster similar dishes [using fuzzy search?]
    pass


def id_main_ingredient(dish):
# identfy main ingredient of a dish
# look for nouns; prep phrases will have been stripped
# if more than 1 noun: noun in list of meats/proteins most likely main
# main ingredient?
    pass


def find_techniques(dish):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods
    dish_words = corpora[dish]
    techniques = []
    for word in dish_words:
        suffix = str(word[-2:])
        if suffix == 'ed':
            techniques.append(word)
    if len(techniques) > 0:
        return techniques
    else:
        return None


# def assign_techniques(corpora):
# should return a dictionary that maps menu items to list of techniques]
#     technique_mappings = {}
#     for id, text in corpora.items():
#       call find techniques
            # for each technique in list that gets returned:
            #     check for technique in technique_mappings
            #         if not there: add as key w/ value = 
            #         list containing item id of dish
            #         if there: append dish ID to end of value list


def id_fancy_foods(dish):
    pass


def id_venue(restaurant):
# identify "restaurants" that are actually ships, railroad cars, etc.
# look for "on board", "en route", "S.S.", etc.
    pass


def id_meal_part(dish):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup? attempt to implement w/ supervised classification -- go through subset
# of dish descriptions, create a training set?
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


if __name__=="__main__":
    corpora = build_dish_corpora()
    lexicon = lexicon_setup()