import model
from datetime import datetime


def find_menus_by_year(year):
    menus = model.session.query(model.Menu).filter(
        model.Menu.date >= datetime(year, 1, 1)).filter(
        model.Menu.date <= datetime(year, 12, 31)).all()
    return menus


def count_menus_by_year(year):
    menu_list = find_menus_by_year(year)
    return len(menu_list)


def count_menus_by_decade(year):
    total = 0
    endyear = year + 10
    while year < (endyear):
        total += count_menus_by_year(year)
        year = year + 1
    return total


def find_similar_restaurant(restaurant):
# find restaurants similar to input restaurant based on comparison of dishes
    pass


def dish_frequency(dish):
# calculate how frequently a dish (or category of dishes?) appears relative
# to total number of dishes for that year
    pass


def count_items(menu):
    pass


def find_similar_dishes(dish, num):
# return a list of <num> dishes that are most similar to <dish>
    pass

def find_random(input):
# return a random restaurant, dish, or item (based on input)
    pass