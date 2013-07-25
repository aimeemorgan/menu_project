import model

#For all duplicate NAMEs in restaurants:
#make the one with the lowest id number the canonical version
#make a dictionary(?) with the id number of the canonical version as the key,
#and the values a list of id numbers of duplicate rows


def restaurant_id_mapping():
# !!!query to get all Restaurant objects from restaurant table
# !!!return as restaurant_list]
    restaurant_names = {}
    id_mapping = {}
    for restaurant in restaurant_list:
        if not (restaurant.name in restaurant_names):   # restaurant is NOT a dup
            restaurant_names[restaurant.name] = restaurant.id
            id_mapping[restaurant.id] = []
        else:  # restaurant IS a dup
            canonical_id = restaurant_names[restaurant.name]
        id_mapping[cannonical_id].append(restaurant.id)
    return id_mapping


def menu_table_replace(id_mapping):
# id mapping needs to be iterator, yes?
# for each key(id) in id_mapping:
#       new_id = id
#       get value (=list of ids)
#           for each item in value:
#                search menus for rows where id=item
#        for each row found:
#             replace id with new_id

         
def restaurant_table_id_replace(id_mapping):
# id mapping needs to be iterator, yes?
# for each key(id) in id_mapping:
#       new_id = id
#       get value (=list of ids)
#           for each item in value:
#                search menus for rows where id=item
#        for each row found:
#             replace id with new_id

def delete_restaurant_dups(id_mapping):
# for each key(id) in id_mapping:
#      get value(=list of ids)
#     for each id in value:
#        delete row in restaurants where id=id



#########################################    
# from http://stackoverflow.com/questions/14471179/find-duplicate-rows-with-postgresql

# DELETE FROM P1
# USING Photos P1, Photos P2
# WHERE P1.id > P2.id
#    AND P1.merchant_id = P2.merchant_id
#    AND P1.url = P2.url;