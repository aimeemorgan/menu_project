import webapp.model as model
import cdecimal
from data_processing import build_dish_corpus, build_menu_corpus


# Python implementaton of basic all-pairs algorithm using cosine similiary
# from 2007 paper by Bayardo et. al.: 
# http://www.bayardo.org/ps/www2007.pdf

## main all pairs function

def all_pairs(corpus, t):
    index = {}
    results = {}
    count = 0
    for item_id, words in corpus.items():
        # store square root of vector size for cosine calculation
        # since words generally don't repeat in item descriptions, can
        # assume that vector size = vector magnitude
        vsize = len(words)
        if vsize != 0:
            sqrt_of_vsize = cdecimal.Decimal(vsize).sqrt()
            matches = find_matches(item_id, sqrt_of_vsize, index, corpus, t)
            for match in matches:
                results[(item_id, match[0])] = match[1]
            for word in words:
                index.setdefault(word, [])
                index[word].append((item_id, sqrt_of_vsize))
            count = count + 1
            print count
    return results


def find_matches(item_id, sqrt_of_vsize, index, corpus, t):
    matches = []
    # pairs w their cosine similarity score where score > threshold
    a = {} 
    # dict a is holding place for compared pairs w their calculated dot products
    words = corpus[item_id]
    for word in words:
        if word in index.keys():  # if word has been seen before
            # find all other items whose description contain that word
            appearances = index[word] 
            # dictionary: word as key, list of (item_ids, sqrt_of_vsize) as value
            for item in appearances:
            # each item = (item_id = item[0], sqrt_of_vsize = item[1]) 
                if item[0] != item_id:
                # don't cmp items to themselves
                    # now add this word's contribution to dot product total
                    # i.e. (# of appearances in first vector * # of 
                    # appearances in second)
                    a.setdefault(item, 0)
                    a[item] += 1 
                    # words don't repeat in vectors, so product always = 1
    for (compared_item, sqrt_of_vsize2), dot_product in a.items():
        denominator = sqrt_of_vsize * sqrt_of_vsize2
        score = dot_product / denominator
        if score >= t:
            matches.append((compared_item, score))
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
                key = ('item_similarities:' + str(item_id))
                model.r.lpush(key, match)
    model.r.save


def persist_menu_matches(results):
    for item_id, matches in results.items():
        for match in matches:
            key = ('menu_similarities:' + str(item_id))
            model.r.lpush(key, match)
    model.r.save





