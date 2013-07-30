import model
import nltk
from lexicon import *
from datetime import datetime


# preprocessing


def build_dish_corpora():
# build a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation.
    pass


def build_menu_corpora():
# build a dictionary where key is menu.id, value is tokenized list
# with text of item.descriptions for all items that appear on menu.
# lowercase/strip punctuation
    pass


def strip_stopwords():
# take a corpora, remove stopwords from nltk stopword set
    pass


def strip_prepositional_phrases():
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    pass


# classification


def classify_dishes(corpora):
# classify dishes
# likely to be function that calls a bunch of subfunctions for various
# classification tasks
    pass


def word_frequency(num):
# find the <num> most frequent words that appear in item descriptions
# (to aid in development of lexicon?)
    pass


def cluster_dishes(corpora):
# cluster similar dishes [using fuzzy search?]
    pass


def id_main_ingredient(corpora):
# identfy main ingredient of a dish
# look for nouns; prep phrases will have been stripped
# if more than 1 noun: noun in list of meats/proteins most likely main
# main ingredient?
    pass


def find_techniques(corpora):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods
    pass


def id_fancy_foods(corpora):
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
#(likely to be called from within classification subfunctions)
###########################################


# helper functions

def find_unclassified(category):
# find dishes that lack a classification term for a given
# category (to aid in refinement of classification)
    pass


def find_menus_by_year(year):
    menus = model.session.query(model.Menu).filter(
        model.Menu.date >= datetime(year, 1, 1)).filter(
        model.Menu.date <= datetime(year, 12, 31)).all()
    return menus


def count_menus_by_year(year):
    menu_list = find_menus_by_year(year)
    return len(menu_list)

def count_menus_by_decade(decade):
    pass


def find_similar_restaurant(restaurant):
# find restaurants similar to input restaurant based on comparison of dishes
    pass


def dish_frequency(dish):
# calculate how frequently a dish (or category of dishes?) appears relative
# to total number of dishes for that year
    pass


def count_items(menu):
    pass

def find_similar_dishes(dish, num):
# return a list of <num> dishes that are most similar to <dish>
    pass
