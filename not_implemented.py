# def dishes_that_appear_with(dish):
# # For a given dish, generate a list of IDs of dishes that frequently
# # appear on the same menu as that dish.
# # so basically, for a given dish ID:
# # 1. get all menus on which that dish appears (there's a function!)
# # 1.5 count all menus on which that dish appears, save count
# # 2. make a blank dictionary
# # 3. for each menu, add each item on the menu to the blank dictionary w count of occurences
# # 4. for each entry in dictionary: replace value with value/menu count to get ratio
# #    (between 0 and 1)
# # 5: make list mapping frequency ratio to dish ID
#     pass
    

# def appears_with_for_corpus(corpus):
# # call above fucntion for every dish in corpus
#     appearances = {}
#     for dish_id, description in corpus.items():
#         appearances [dish_id] = dishes_that_appear_with(dish_id)
#     return appearances


# functions to not build unless lots of extra time


# def id_fancy_foods(dish):
#     pass


# def id_venue(restaurant):
# # identify "restaurants" that are actually ships, railroad cars, etc.
# # look for "on board", "en route", "S.S.", etc.
#     pass

# def id_main_ingredient(dish):
# # identfy main ingredient of a dish
# # look for nouns; prep phrases will have been stripped
# # if more than 1 noun: noun in list of meats/proteins most likely main
# # main ingredient?
#     pass


# def ingredients_for_corpus(corpus):
#     pass


# def map_ingredients_to_dishes():
#     pass


# def find_ingredient_frequencies():
#     pass