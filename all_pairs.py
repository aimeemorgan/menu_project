import model
import cdecimal
from data_processing import build_dish_corpus, build_menu_corpus


## main all pairs function

def all_pairs(corpus, t):
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
            for item in appearances:  # each item = (item_id, decimal)
                if item[0] != item_id:  # don't cmp items to themselves
                    a.setdefault(item[0], 0)
                    a[item[0]] += (item[1] * weight)
    for item_id, score in a.items():
        if score >= t:
            matches.append((item_id, item[0]))
    return matches


def match_dictionary_for_db(results):
    print len(results)
    matches = {}
    for pair, score in results.items():
        print pair
        matches.setdefault(pair[0], [])
        matches.setdefault(pair[1], [])
        if pair[1] not in matches[pair[0]]:
            matches[pair[0]].append(pair[1])
        if pair[0] not in matches[pair[1]]:
            matches[pair[1]].append(pair[0])
    return matches


def persist_matches(results):
    for item_id, matches in results.items():
        for match in matches:
            if match != item_id:
                key = ('similarities_item:' + str(item_id))
                model.r.lpush(key, match)
    model.r.save


def persist_menu_matches(results):
    for item_id, matches in results.items():
        for match in matches:
            key = ('similarities_menu:' + str(item_id))
            model.r.lpush(key, match)
    model.r.save





