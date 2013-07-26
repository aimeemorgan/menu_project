import model


def classify_dishes():
# classify dishes
    pass


def cluster_dishes():
# cluster similar dishes
    pass


def find_similar_restaurant(restaurant):
# find restaurants similar to input restaurant based on comparison of dishes
    pass


def dish_frequency(dish):
# calculate how frequently a dish (or category of dishes?) appears relative
# to total number of dishes for that year
    pass


def find_unclassified(category):
# find dishes that lack a classification term for a given
# category (to aid in refinement of classification)
    pass


def strip_prepositional_phrases():
# strip out prepositional phrases as pre-classification step
# (i.e. "with...", "in..." "accompanied by...")
    pass


def find_techniques():
# identify verbs in dish descriptions as a way of classifying
# by preparation methods
    pass


# some kind of master function for reading classification info
# from dictionaries, writing to csv files for import to database
# for webapp.


def strip_stopwords():
# take a corpora, remove stopwords from nltk stopword set
    pass


def build_dish_corpora():
# build a dictionary where key is item.id, value is item.description
# as a tokenized list.
    pass


def build_menu_corpora():
# build a dictionary where key is menu.id, value is tokenized list
# with text of item.descriptions for all items that appear on menu
    pass

