import model
import nltk
import redis
import re
from controller import find_menus_by_year, find_menus_by_decade
from nltk.corpus import stopwords
#from lexicon import lexicon_names, lexicon_setup

# preprocessing

def build_itemid_index():
    item_list = model.session.query(model.Item).all()
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for item in item_list:
        r.lpush('itemid_index', item.id)
    r.save


def build_dish_corpus():
# builds a dictionary where key is item.id, value is item.description
# as a tokenized list. lowercase/strip punctuation, strip stopwords
    dish_list = model.session.query(model.Item).all()
    dish_corpus = {}
    for dish in dish_list:
        text = (dish.description).lower().strip().strip('*')
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
        tokens = []
        for item in menu.items:
            if item.item:
                text = (item.item.description).lower().strip()
                stripped_text = re.sub('[^A-Za-z0-9]+', ' ', text)
                new_tokens = nltk.word_tokenize(stripped_text)
                stoplist = stopwords.words('english')
                for token in new_tokens:
                    if token in stoplist:
                        tokens.remove(token)
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
    r = redis.StrictRedis(host='holocalhost', port=6379, db=0)
    items = most_popular[year] 
    for item in items:
        key = ('popular_year:%s') % year
        r.lpush(key, item)
    r.save


def persist_most_popular_decades(decade, most_popular):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    items = most_popular[decade] 
    for item in items:
        key = ('popular_decade:%s') % decade
        r.lpush(key, item)
    r.save



# helper functions

def find_unclassified(category):
# find dishes that lack a classification term for a given
# category (to aid in refinement of classification)
    pass


