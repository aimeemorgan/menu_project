import model
from datetime import datetime
from random import randint

# functions to get menus / menu info


def count_menus_by_year(year):
    menu_list = find_menus_by_year(year)
    return len(menu_list)


def count_menus_by_decade(year):
    total = 0
    endyear = year + 10
    while year < endyear:
        total += count_menus_by_year(year)
        year += 1
    return total


def count_menus_by_years(year):
# input is starting year of decade (i.e. 1960 for 1960s)
    counts = {}
    endyear = year + 10
    while year < endyear:
        count = count_menus_by_year(year)
        counts[year] = count
        year += 1
    return counts

def counts_for_all_decades():
# for map dislay: return list of lists of (decade, count)
    decade_list = []
    for year in range(1850, 2010, 10):
        count = count_menus_by_decade(year)
        decade_list.append([year, count])
    return decade_list


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
    return menu_list


def get_total_menus():
    count = model.session.query(model.Menu).count()
    return count


def get_random_menu():
    count = get_total_menus()
    num = randint(12463, count)
    menu = model.session.query(model.Menu).get(num)
    if menu == None:
        get_random_menu()
    return menu


# functions to get restaurants / restautant info


def find_restaurant_by_name(name):
    restaurant = model.session.query(model.Restaurant).filter(model.Restaurant.name.like('%' + name + '%')).all()
    return restaurant


def location_same_as_name(restaurant):
    return restaurant.name == restaurant.location


# functions to get dishes / dish info


def find_dishes_by_keyword(keyword):
    dish = model.session.query(model.Item).filter(model.Item.description.like('%' + keyword + '%')).all()
    return dish

def find_dishes_by_technique(technique):
    


def find_dishes_by_category(category):
    pass


def count_dish_by_year(dish, year):
# return count of how frequently a dish appears in given year.
    pass


def dish_frequency_by_year(dish, year):
# calculate how frequently a dish (or category of dishes?) appears relative
# to total number of dishes for that year
    pass


def count_dish_by_decade(dish, year):
    pass


def dish_frequency_by_decade(dish, decade):
    pass


def get_similar_dishes(dish, num):
# return a list of <num> dishes that are most similar to <dish>
# (based on fuzzy text search score)
# (precalculate and persist this in database)
    pass


def get_total_dishes():
    count = model.session.query(model.Item).count()
    return count


def get_random_dish():
    count = get_total_dishes()
    num = randint(1, count)
    dish = model.session.query(model.Item).get(num)
    if dish == None:
        get_random_dish()
    return dish


