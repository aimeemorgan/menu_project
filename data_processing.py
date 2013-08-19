import model
import nltk
import re
import helper
from nltk.corpus import stopwords
#from lexicon import lexicon_names, lexicon_setup

# preprocessing

def build_itemid_index():
# save a list of all itemid numbers to redis
    item_list = model.session.query(model.Item).all()
    for item in item_list:
        model.r.lpush('itemid_index', item.id)
    model.r.save


def build_dish_corpus():
# build a dictionary where key is item.id, value is item.description
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
# build a corpus where each menu's item desriptions are
# grouped together as a document
    menu_list = model.session.query(model.Menu).all()
    menu_corpus = {}
    count = 0
    for menu in menu_list:
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
        count += 1
        print count
        menu_corpus[menu.id] = tokens
    return menu_corpus


def persist_corpus(name, corpus):
# save corpus to redis
    for item_id, tokens in corpus.items():
        for token in tokens:
            key = (name + ':%s') % str(item_id)
            model.r.lpush(key, token)
    model.r.save


def load_corpus(item_index_name, corpus_prefix):
# load a corpus from redis
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
# save a list of all words in a corpus to redis
    for word in freq.keys():
        model.r.lpush('word_index', word)
    model.r.save


def persist_word_frequencies(frequencies):
# save word frequencies for a corpus to redis
    for word, freq in frequencies.items():
            key = ('frequency:%s') % word
            model.r.lpush(key, freq)
    model.r.save


def load_word_frequencies():
# load word frequencies for a corpus from redis
    index = model.r.lrange('word_index', 0, -1)
    freq = {}
    for word in index:
        key =  'frequency:%s' % word
        value = model.r.lrange(key, 0, -1)
        freq[word] = value
    return freq


def most_frequent_sorted(frequencies):
# return a list of corpus words sorted by frequency
# of appearance in corpus
    ranked_freq = []
    for word, count in frequencies.items():
        ranked_freq.append((count, word))
    return sorted(ranked_freq)


def technique_stoplist():
# build a list of stopwords for use in determining
# item cooking techniques (i.e., words that do not indicate
# technique)
    stoplist = {}
    filepath = './lexicon/technique_stoplist.txt'
    f = open(filepath)
    for row in f:
        new_entry = row.strip().lower()
        stoplist[new_entry] = 1
    print stoplist
    return stoplist


def id_techniques(dish_id, corpus, stoplist):
# identify verbs in dish descriptions as a way of classifying
# by preparation methods.
    dish_words = corpus[dish_id]
    techniques = []
    stoplist = {}
    for word in dish_words:
        if word == 'roast':
            techniques.append('roasted')
        if word == 'sautee':
            techniques.append('sauteed')
        if len(word) > 2:
            suffix = (word[-2:])
            if suffix == 'ed':
                if word not in stoplist:
                    techniques.append(word)
    if len(techniques) > 0:
        return techniques
    else:
        return ['unknown']


def techniques_for_corpus(corpus, stoplist):
# identify techniques for all of the items in a corpus
# save results to redis
    for dish_id, text in corpus.items():
        techniques = id_techniques(dish_id, corpus, stoplist)
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
    menus = helper.find_menus_by_year(year)
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


def most_popular_all_years():
# return a dict where key = year, value = list of 10 most
# popular dishes
    most_popular = {}
    for year in range(1850, 2010):
        items = most_popular_dishes(year)
        most_popular.setdefault(year, [])
        if items:
            for item in items:
                if item != None:
                    most_popular[year].append(item[1].id)
            persist_most_popular_years(year, most_popular)
    return most_popular


def most_popular_dishes_decade(decade):
# return a list of the most popular dishes for a given decade
    menus = helper.find_menus_by_decade(decade)
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


def most_popular_all_decades():
# generate lists of the most popular items for all decades in
# the dataset. save results to redis.
    for decade in range(1850, 2011, 10):
        popular = most_popular_dishes_decade(decade)
        if popular:
            results = []
            for item in popular:
                result = item[1].id
                results.append(result)
            persist_most_popular_decades(decade, results)
            print decade, results
        else:
            persist_most_popular_decades(decade, ['no popular items found'])
    return "SUCCESS"


def persist_most_popular_years(year, most_popular):
## called from within most_popular_all_years; helper
# function to save results for a decade to redis.
    items = most_popular[year] 
    for item in items:
        key = ('popular_year:%s') % year
        model.r.lpush(key, item)
    print "PERSISTED: ", year 
    model.r.save


def persist_most_popular_decades(decade, items):
# called from within most_popular_all_decades; helper
# function to save results for a decade to redis.
    for item in items:
        key = ('popular_decade:%s') % decade
        model.r.lpush(key, item)
    print "PERSISTED: ", decade   
    model.r.save


def persist_decade_counts_for_chart():
# generate and save counts of total menus for
# each decade in the dataset. for use in chart on main page of site.
    for year in range(1850, 2010, 10):
        print year
        menu_count = helper.total_menus_per_decade(year)
        print menu_count
        key = ('decade_count_menus:%s') % year
        model.r.set(key, menu_count)
        print year, "PERSISTED!!!"
    model.r.save


def persist_year_counts_for_chart():
# generate and save counts of total menus for
# each decade in the dataset. for use in chart on main page of site.
    for year in range(1850, 2010):
        print year
        menu_count = helper.count_menus_by_year(year)
        print menu_count
        key = ('year_count_menus:%s') % year
        model.r.set(key, menu_count)
        print year, "PERSISTED!!!"
    model.r.save


