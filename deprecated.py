# functions that are no longer being used in data_processing

# def find_similar_restaurant(restaurant):
## find restaurants similar to input restaurant based on comparison of dishes
# # this should be precalculated, persisted -- move to data processing?
# 1. get menu list for restaurant
# 2. for other 

# def build_dish_corpus_bag():
# # builds a dictionary where key is item.id, value is item.description
# # as a tokenized list. lowercase/strip punctuation.
#     dish_list = model.session.query(model.Item).all()
#     dish_corpus = {}
#     for dish in dish_list:
#         text = (dish.description).lower().strip().strip('*')
#         tokens = nltk.word_tokenize(text)
#         bag = bag_of_words(tokens)
#         dish_corpus[dish.id] = bag
#     return dish_corpus


# def bag_of_words(words):
#     return dict([word, True] for word in words)

# def find_similarity_scores(item_id, dish_corpus):
# # for a given dish, use fuzzy search to calculate similarity scores
# # for other dishes in the corpus. 
#     scores = {}
#     comparison_desc = dish_corpus[item_id]
#     for item, desc in dish_corpus.items():
#         if item_id != item:
#             score = fuzz.token_set_ratio(comparison_desc, desc)
#             if score >= 90:
#                 scores[item] = score
#     return scores


# def rank_similarities(scores):
#     ranked_scores = []
#     for item, score in scores.items():
#         ranked_scores.append((score, item))
#     ranked_scores = sorted(ranked_scores, reverse=True)
#     top_25 = ranked_scores[0:25]
#     print top_25
#     return top_25


# def similar_dishes_for_corpus(dish_corpus):
# Return a dictionary with each dish ID from corpus mapped to a list of dish IDs
# of 25 similar dishes, ordered in descending order of similarity.
# refactor so that dishes are removed from the corpus as they are matched
    # similarities = {}
    # for dish_id in dish_corpus.keys():
    #     scores = find_similarity_scores(dish_id, dish_corpus)
    #     top_25 = rank_similarities(scores)    
    #     similarities[dish_id] = top_25
    # return similarities

# refactor to persist in redis
# def persist_similarities(similarities):
#     for dish_id, ranked_scores in similarities:
#         similarity_id = 0
#         for item in ranked_scores:
#             new_similarity = new_itemsimilarity = model.ItemSimilarity(
#                                                     id = similarity_id,
#                                                     item_id_1 = dish_id,
#                                                     item_id_2 = item[1],
#                                                     score = item[0])
#             session.add(new_similarity)
#             session.commit()

# def dish_corpus_to_bag(corpus):
# # takes basic dish corpus, returns a dictionary where key is item.id, 
# # value is item.description as a bag of words.
#     bag_corpus = {}
#     for item_id, tokens in corpus.items():
#         bag = bag_of_words(tokens)
#         bag_corpus[item_id] = bag
#     return bag_corpus


# def bag_of_words(words):
#     return list((word, True) for word in words)


# build inverted list representation: a dictionary with keys
# equal to words in word_index

# def build_inverted_list(freq, corpus):
#     inverted = {}
#     for word in freq.keys():
#         print word
#         inverted.setdefault(word, [])
#     for item_id, tokens in corpus.items():
#         print item_id, tokens
#         for item in tokens:
#             inverted[item].append((item_id, (1 / decimal.Decimal(len(tokens)))))
#     return inverted

# def all_pairs_naive(corpus, t, inverted):
#     results = {}
#     count = 0
#     for item_id  in corpus.keys():
#         matches = find_matches_naive(item_id, inverted, corpus, t)
#         print matches
#         results[item_id] = matches
#         count += 1
#         print count
#     return results


# def find_matches_naive(item_id, inverted, corpus, t):
#     matches = []
#     a = {}
#     words = corpus[item_id]
#     for word in words:
#         appearances = inverted[word] 
#         for item in appearances:  # each item = (item_id, float)
#             if item[0] != item_id:  # don't cmp items to themselves
#                 a.setdefault(item[0], 0)
#                 a[item[0]] += decimal.Decimal(
#                                 item[1] * (1 / decimal.Decimal(len(words))))
#     for item_id, score in a.items():
#         print score
#         if score >= t:
#             matches.append((item_id, score))
#     return matches

# def build_dish_corpus_no_tokens():
# # for fuzzy search
#     dish_list = model.session.query(model.Item).all()
#     dish_corpus = {}
#     for dish in dish_list:
#         text = (dish.description).lower().strip().strip('*')
#         dish_corpus[dish.id] = text
#     return dish_corpus

# def strip_stopwords(corpus):
# # take a corpus, remove stopwords from nltk stopword set
#     stoplist = stopwords.words('english')
#     print stoplist
#     for entry in stoplist:
#         entry = entry.encode('utf-8')
#     corpus = dict(corpus)
#     for dish, description in corpus.items():
#         for word in description:
#             if word in stoplist:
#                 description.remove(word)
#         corpus[dish] = description
#     return corpus