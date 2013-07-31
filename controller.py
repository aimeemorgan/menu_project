import model
from datetime import datetime

# functions to get menus / menu info


def count_menus_by_year(year):
    menu_list = find_menus_by_year(year)
    return len(menu_list)


def count_menus_by_decade(year):
    total = 0
    endyear = year + 10
    while year < endyear:
        total += count_menus_by_year(year)
        year = year + 1
    return total


def count_menus_by_years(decade):
    pass


def find_menus_by_year(year):
    menus = model.session.query(model.Menu).filter(
        model.Menu.date >= datetime(year, 1, 1)).filter(
        model.Menu.date <= datetime(year, 12, 31)).all()
    return menus


def find_menus_by_decade(year):
    endyear = year + 10
    menu_list = []
    while year < endyear:
        menus = find_menus_by_year(year)
        for menu in menus:
            menu_list.append(menu)



# functions to get restaurants / restautant info


def find_restaurant_by_name(name):
    restaurant = model.session.query(model.Restaurant).filter(model.Restaurant.name.like('%' + name + '%')).all()
    return restaurant


def find_similar_restaurant(restaurant):
# find restaurants similar to input restaurant based on comparison of dishes
    pass


# functions to get dishes / dish info


def find_dish_keyword(keyword):
    dish = model.session.query(model.Item).filter(model.Item.description.like('%' + keyword + '%')).all()
    return dish


def dish_frequency_by_year(dish, year):
# calculate how frequently a dish (or category of dishes?) appears relative
# to total number of dishes for that year
    pass


def dish_frequency_by_decade(dish, decade):
    pass


def get_similar_dishes(dish, num):
# return a list of <num> dishes that are most similar to <dish>
# (based on fuzzy text search score)
# (precalculate and persist this in database)
    pass


def find_random(input):
# return a random restaurant, menu, or item (based on input)
    pass