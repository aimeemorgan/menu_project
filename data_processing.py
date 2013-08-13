import model
import nltk
import re
from controller import find_menus_by_year, find_menus_by_decade
from nltk.corpus import stopwords
#from lexicon import lexicon_names, lexicon_setup

# preprocessing

def build_itemid_index():
    item_list = model.session.query(model.Item).all()
    for item in item_list:
        model.r.lpush('itemid_index', item.id)
    model.r.save


def build_dish_corpus():
# builds a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation, strip stopwords
    dish_list = model.session.query(model.Item).all()
    dish_corpus = {}
    for dish in dish_list:
        text = (dish.description).lower().strip()
        stripped_text = re.sub('[^A-Za-z0-9]+', ' ', text)
        tokens = nltk.word_tokenize(stripped_text)
        stoplist = stopwords.words('english')
        for token in tokens:
            if token in stoplist:
                tokens.remove(token)
        dish_corpus[dish.id] = tokens
    return dish_corpus

   
def build_menu_corpus(): 
    menu_list = model.session.query(model.Menu).all()
    menu_corpus = {}
    for menu in menu_list:
        print menu.id
        items = menu.get_items()
        tokens = []
        for item in items:
            if item != None:
                text = (item.description).lower().strip()
                stripped_text = re.sub('[^A-Za-z0-9]+', ' ', text)
                new_tokens = nltk.word_tokenize(stripped_text)
                stoplist = stopwords.words('english')
                for token in new_tokens:
                    if token not in stoplist:
                        tokens.append(token)
        print tokens
        menu_corpus[menu.id] = tokens
    return menu_corpus


def persist_corpus(name, corpus):
    for item_id, tokens in corpus.items():
        for token in tokens:
            key = (name + ':%s') % str(item_id)
            model.r.lpush(key, token)
    model.r.save


def load_corpus(item_index_name, corpus_prefix):
    index = model.r.lrange(item_index_name, 0, -1)
    corpus = {}
    for item in index:
        key =  corpus_prefix + ':%s' % item
        values = model.r.lrange(key, 0, -1)
        corpus[int(item)] = values
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
    for word in freq.keys():
        model.r.lpush('word_index', word)
    model.r.save


def persist_word_frequencies(frequencies): 
    for word, freq in frequencies.items():
            key = ('frequency:%s') % word
            model.r.lpush(key, freq)
    model.r.save


def load_word_frequencies():
    index = model.r.lrange('word_index', 0, -1)
    freq = {}
    for word in index:
        key =  'frequency:%s' % word
        value = model.r.lrange(key, 0, -1)
        freq[word] = value
    return freq


def most_frequent_sorted(frequencies):
    ranked_freq = []
    for word, count in frequencies.items():
        ranked_freq.append((count, word))
    return sorted(ranked_freq)


def id_techniques(dish_id, corpus):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods.
    dish_words = corpus[dish_id]
    techniques = []
    false_matches = {'n': 0, 'bed': 0, 'red': 0, 'served': 0, 'assorted': 0, 
                    'selected': 0, 'imported': 0, 'w': 0, 'o': 0,'k': 0,'u': 0,}
    for word in dish_words:
        if len(word) > 2:
            suffix = (word[-2:]).encode('utf-8')
            if suffix == 'ed':
                if word not in false_matches:
                    techniques.append(word)
    if len(techniques) > 0:
        return techniques
    else:
        return ['unknown']


def techniques_for_corpus(corpus):
    for dish_id, text in corpus.items():
        techniques = id_techniques(dish_id, corpus)
        if techniques:
            for technique in techniques:
                # add technique tags to dish, persist to redis
                dish_key = ('item_techniques:' + str(dish_id))
                model.r.lpush(dish_key, technique)
                # add dish_id to technique list, persist to redis
                technique_key = ('technique_items:' + str(technique))
                model.r.lpush(technique_key, dish_id)
                model.r.save
    


def most_popular_dishes(year):
# for a given year, get list of dishes ordered by
# how often they appear on menus
    menus = find_menus_by_year(year)
    all_items = {}
    frequencies = []
    for menu in menus:
        items = menu.get_items()
        for item in items:
            if item != False:
                all_items.setdefault(item, 0)
                all_items[item] +=1
    for item, count in all_items.items():
        frequencies.append((count, item))
    frequencies = sorted(frequencies, reverse=True)
    return frequencies[0:10]


def most_popular_dishes_decade(decade):
    menus = find_menus_by_decade(decade)
    all_items = {}
    frequencies = []
    for menu in menus:
        items = menu.get_items()
        for item in items:
            if item != False:
                print item
                all_items.setdefault(item, 0)
                all_items[item] +=1
    for item, count in all_items.items():
        frequencies.append((count, item))
    frequencies = sorted(frequencies, reverse=True)
    return frequencies[0:10]


def most_popular_all_years():
# return a dict where key = year, value = list of 10 most
# popular dishes
    most_popular = {}
    for year in range(1949, 2010):
        items = most_popular_dishes(year)
        most_popular.setdefault(year, [])
        if items:
            for item in items:
                if item != None:
                    most_popular[year].append(item[1].id)
            persist_most_popular_years(year, most_popular)
            print year, most_popular[year]
    return most_popular


def most_popular_all_decades():
    most_popular = {}
    for decade in range(1850, 2011, 10):
        items = most_popular_dishes_decade(decade)
        most_popular.setdefault(decade, [])
        if items:
            for item in items:
                if item != None:
                    print item
                    most_popular[decade].append(item[1].id)
            persist_most_popular_decades(decade, most_popular)
            print decade, most_popular[decade]
    return most_popular


def persist_most_popular_years(year, most_popular):
    items = most_popular[year] 
    for item in items:
        key = ('popular_year:%s') % year
        model.r.lpush(key, item)
    model.r.save


def persist_most_popular_decades(decade, most_popular):
    items = most_popular[decade] 
    for item in items:
        key = ('popular_decade:%s') % decade
        model.r.lpush(key, item)
    model.r.save



# helper functions


def match_dictionary_for_database(results):
    print len(results)
    matches = {}
    for pair, score in results.items():
        print pair
        matches.setdefault(pair[0], [])
        matches.setdefault(pair[1], [])
        matches[pair[0]].append(pair[1])
        matches[pair[1]].append(pair[0])
    return matches



def persist_matches_dishes(results):
    for item_id, matches in results.items():
        for match in matches:
            key = ('similarities_item:' + str(item_id))
            model.r.lpush(key, match)
    model.r.save
