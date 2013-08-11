import model
import nltk
import redis
import re
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


def id_category(dish, corpus):
# is this dish an entree? a side dish? dessert? breakfast? beverage? salad?
# soup? attempt to implement w/ supervised classification -- go through subset
# of dish descriptions, create a training set?
    # for dish, tokens in corpus.items():
    #     for word in tokens:
    #         if [word in lexicon]
          # for word in tokens:
    pass


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

