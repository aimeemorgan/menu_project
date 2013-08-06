import model

#For all duplicate NAMEs in restaurants:
#make the one with the lowest id number the canonical version
#make a dictionary(?) with the id number of the canonical version as the key,
#and the values a list of id numbers of duplicate rows


def restaurant_id_mapping():
    restaurant_list = model.session.query(model.Restaurant).all()
    restaurant_names = {}
    id_mapping = {}
    for restaurant in restaurant_list:
        if not (restaurant.name in restaurant_names):   # restaurant is NOT a dup
            restaurant_names[restaurant.name] = restaurant.id
            id_mapping[restaurant.id] = []
        else:  # restaurant IS a dup
            canonical_id = restaurant_names[restaurant.name]
            id_mapping[canonical_id].append(restaurant.id)
    return id_mapping


def menu_table_replace(id_mapping):
    for canonical_id, other_ids in id_mapping.items():
        for id in other_ids:
            menu_list = model.session.query(model.Menu).filter(
                                            model.Menu.restaurant_id==id).all()
            for menu in menu_list:
                menu.restaurant_id = canonical_id
                model.session.add(menu)
    model.session.commit()


def delete_restaurant_dups(id_mapping):
    for canonical_id, other_ids in id_mapping.items():
        for id in other_ids:
            model.session.query(model.Restaurant).filter(
                            model.Restaurant.id==id).delete()
    model.session.commit()




# seasons = model.find_restaurant_by_name('Four Seasons')
# for restaurant in seasons:
#     print restaurant.id
#     print restaurant.show_menus()