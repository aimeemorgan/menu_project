import model
import nltk
import redis
import re
import cdecimal
from nltk.corpus import stopwords


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


## main all pairs function

def all_pairs(corpus, t):
# refactor to save results directly into redis?
    index = {}
    results = {}
    count = 0
    for item_id, words in corpus.items():
        matches = find_matches(item_id, index, corpus, t)
        try:
            weight = (cdecimal.Decimal(1) / (len(words)))
        except:
            weight = 1
        for match in matches:
            results[(match[0], match[1])] = match[2]
        for word in words:
            index.setdefault(word, [])
            index[word].append((item_id, weight))
        count = count + 1
        print count
    return results


def find_matches(item_id, index, corpus, t):
    matches = []
    a = {}
    words = corpus[item_id]
    for word in words:
        weight = (cdecimal.Decimal(1) / (len(words)))
        if word in index.keys():  # if word has been seen before
            appearances = index[word] 
            for item in appearances:  # each item = (item_id, float)
                if item[0] != item_id:  # don't cmp items to themselves
                    a.setdefault(item[0], 0)
                    a[item[0]] += (item[1] * weight)
    for item_id, score in a.items():
        if score >= t:
            matches.append((item_id, item[0], score))
    return matches


def test_matches(item_id, matches):
    for match in matches:
        if item_id in match:
            for item in match:
                if item != item_id:
                    item = model.session.query(model.Item).get(item)
                    print item


def match_dictionary_for_db(results):
    print len(results)
    matches = {}
    for pair, score in results.items():
        print pair
        matches.setdefault(pair[0], [])
        matches.setdefault(pair[1], [])
        matches[pair[0]].append(pair[1])
        matches[pair[1]].append(pair[0])
    return matches



def persist_matches(results):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for item_id, matches in results.items():
        for match in matches:
            key = ('similarities_item:' + str(item_id))
            r.lpush(key, match)
    r.save

### compute menu similarities

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
                        new_tokens.remove(token)
                tokens.append(new_tokens)
        menu_corpus[menu.id] = tokens
    return menu_corpus

# word frequency function -- can use above
# all pairs, find matches -- use above
# ngrams as future refinement?

def persist_menu_matches(results):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for item_id, matches in results.items():
        for match in matches:
            key = ('similarities_menu:' + str(item_id))
            r.lpush(key, match)
    r.save





