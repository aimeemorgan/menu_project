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


def counts_for_all_years(startyear):
# for chart dislay: return list of lists of (year, count) for decade
# indicated by stopyear.
    endyear = startyear + 10
    yearlist = [['Year', 'link', 'Menu Count']] 
    for year in range(startyear, endyear):
        count = count_menus_by_decade(year)
        link = '../year/%s' % str(year)
        yearlist.append([str(year), link, count])
    return yearlist


def counts_for_all_decades():
# for chart dislay: return list of lists of (decade, count)
    decade_list = [['Decade', 'link', 'Menu Count']] 
    for year in range(1850, 2010, 10):
        link = '../decade/%s' % str(year)
        count = count_menus_by_decade(year)
        decade_list.append([str(year), link, count])
    return decade_list


def find_menus_by_year(year, limit=False):
    if (limit is not False) and (type(limit) == int):
        menus = model.session.query(model.Menu).filter(
            model.Menu.date >= datetime(year, 1, 1)).filter(
            model.Menu.date <= datetime(year, 12, 31)).limit(limit)
    else:
        menus = model.session.query(model.Menu).filter(
            model.Menu.date >= datetime(year, 1, 1)).filter(
            model.Menu.date <= datetime(year, 12, 31)).all()
    return menus


def find_menus_by_decade(year, limit=False):
    endyear = year + 10
    menu_list = []
    for year in range(year, endyear):
        menus = find_menus_by_year(year)
        for menu in menus:
            menu_list.append(menu)
            print menu
    return menu_list


def get_total_menus():
    count = model.session.query(model.Menu).count()
    return count


def get_random_menu():
    count = get_total_menus()
    num = randint(12463, count+12463)
    menu = model.session.query(model.Menu).get(num)
    if menu == None:
        menu = get_random_menu()
    return menu


def get_similar_menus(menu_id):
# return list of dishes that are most similar to <dish>
    key  = ('menu_similarities:' + str(menu_id))
    results = model.r.lrange(key, 0, -1)
    results_by_score = [(s[1], s[0]) for s in results]
    sorted_by_score = sorted(results_by_score)
    results = [s[1] for s in sorted_by_score]
    return results


# functions to get restaurants / restautant info


def find_restaurant_by_name(name):
    restaurants = model.session.query(model.Restaurant).filter(
                    model.Restaurant.name.like('%' + name + '%')).all()
    if restaurants == []:
        restaurants = ['no results found']
    return restaurants


def location_same_as_name(restaurant):
    return restaurant.name == restaurant.location


def get_total_restaurants():
    count = model.session.query(model.Restaurant).count()
    return count


def get_random_restaurant():
    count = get_total_menus()
    num = randint(1, count+1)
    restaurant = model.session.query(model.Restaurant).get(num)
    if restaurant == None:
        restaurant = get_random_restaurant()
    return restaurant


# functions to get dishes / dish info


def find_dishes_by_keyword(keyword, limit=False):
    if (limit is not False) and (type(limit) == int):
        dishes = model.session.query(model.Item).filter(
            model.Item.description.like('%' + keyword + '%')).limit(limit)
    else:
        dishes = model.session.query(model.Item).filter(
                    model.Item.description.like('%' + keyword + '%')).all()
    if dishes == []:
        dishes = ['no results found']
    return dishes


def find_dishes_by_technique(technique, limit=False):
    key = ('technique_items:') + technique
    if (limit is not False) and (type(limit) == int):
        items = model.r.lrange(key, 0, limit-1)
    else: 
        items = model.r.lrange(key, 0, -1)
    dishes = []
    for item in items:
        item_id = int(item)
        dish = model.session.query(model.Item).get(item_id)
        dishes.append(dish)
    return dishes


def find_dishes_select_categories():
# for use on Explore Categories page
# for each category in categories, returns a tuple with
# category name, count of dishes in category, and three dishes
# in that category.
    categories =    {'Breakfast': 0,
                     'Dessert': 0,
                     'Fruit': 0,
                     'Fruit': 0,
                     'Meat': 0,
                     'Poultry': 0,
                     'Pasta': 0,
                     'Seafood': 0,
                     'Soup': 0,
                     'Vegetable': 0,
                    }

    results = []
    for category in categories.keys():
        category_lowercase = category.lower()
        dishes = find_three_dishes_by_category(category_lowercase)
        print dishes
        results.append((category, dishes))
    return results


def find_three_dishes_by_category(category):
    key = ('category_items:' + category)
    length = len(model.r.lrange(key, 0, -1))
    seed = randint(0, length)
    items = model.r.lrange(key, seed, seed+2)
    dishes = []
    for item in items:
        item_id = int(item)
        dish = model.session.query(model.Item).get(item_id)
        dishes.append(dish)
    return dishes


def find_dishes_select_techniques():
# for use on Explore Techniques page
# for each technique in techniques, returns a tuple with
# technique name, count of dishes in technique, and three dishes
# in that technique.
    techqniues =    {'Braised': 0,
                     'Boiled': 0,
                     'Broiled': 0,
                     'Carmelized': 0,
                     'Coddled': 0,
                     'Deviled': 0,
                     'Fried': 0,
                     'Mashed': 0,
                     'Poached': 0,
                     'Sauteed': 0,
                     'Steamed': 0,
                     'Stuffed': 0,
                     'Toasted': 0,
                     'Whipped': 0
                    }

    results = []
    for technique in techqniues.keys():
        technique_lowercase = technique.lower()
        dishes = find_three_dishes_by_technique(technique_lowercase)
        print dishes
        results.append((technique, dishes))
    return results


def find_three_dishes_by_technique(technique):
    key = ('technique_items:' + technique)
    length = len(model.r.lrange(key, 0, -1))
    seed = randint(0, length)
    items = model.r.lrange(key, seed, seed+2)
    dishes = []
    for item in items:
        item_id = int(item)
        dish = model.session.query(model.Item).get(item_id)
        dishes.append(dish)
    return dishes


def find_dishes_by_category(category, limit=False):
    key = ('category_items:') + category
    if (limit is not False) and (type(limit) == int):
        items = model.r.lrange(key, 0, limit-1)
    else: 
        items = model.r.lrange(key, 0, -1)
    dishes = []
    for item in items:
        item_id = int(item)
        dish = model.session.query(model.Item).get(item_id)
        dishes.append(dish)
    return dishes


def get_techniques_for_dish(item_id):
    key = ('item_techniques:') + str(item_id)
    techniques = model.r.lrange(key, 0, -1)
    return techniques


def get_categories_for_dish(item_id):
    key = ('item_categories:' + str(item_id))
    categories = model.r.lrange(key, 0, -1)
    return categories


def count_dish_by_year(dish, year):
# return count of how frequently a dish appears in given year.
    count = 0
    for i in dish.menus:
        date = i.menu.date
        print date
        if (date >= datetime(year, 1, 1)) and (
                date <= datetime(year, 12, 31)):
            count += 1
            print count
    return count


def total_dishes_per_year(year):
# not unique; total number of menu items per year
    count = 0
    menus = find_menus_by_year(year)
    for menu in menus:
        count += menu.count_items()
    return count


def dish_frequency_by_year(dish, year):
    dish_total = float(count_dish_by_year(dish, year))
    year_total = float(total_dishes_per_year())
    if year_total != 0:
        return dish_total / year_total
    else:
        return 0


def count_dish_by_decade(dish, year):
    endyear = year + 10
    count = 0
    for year in range (year, endyear):
        count += count_dish_by_year(count, year)
    return count


def total_dishes_per_decade(year):
    total = 0
    endyear = year + 10
    for year in range(year, endyear):
        total += total_dishes_per_year(year)
    return total


def get_popular_dishes_year(year):   
    results = model.r.lrange(('popular_year:' + str(year)), 0, -1)
    popular_items = []
    for result in results:
        item_id = int(result)
        item = model.session.query(model.Item).get(item_id)
        popular_items.append(item)
    return popular_items


def get_popular_dishes_decade(decade):   
    results = model.r.lrange(('popular_decade:' +str(decade)), 0, -1)
    popular_items = []
    for result in results:
        item_id = int(result)
        item = model.session.query(model.Item).get(item_id)
        popular_items.append(item)
    return popular_items


# move these to data_processing, persist in redis, write
# new controller functions to retrieve
# def dish_frequency_by_decade(dish, year):
#     dish_total = float(count_dish_by_decade(dish, year))
#     decade_total = float(total_dishes_per_decade(year))
#     return dish_total / decade_total


# def dish_frequency_decade_for_corpus(year, corpus):
#     dish_frequencies = {}
#     for dish in corpus:
#         dish_frequencies[dish] = dish_frequency_by_decade(dish, year)
#     return dish_frequencies


# def dish_frequency_decade_sorted(dish_frequencies):
#     freq = []
#     for dish, frequency in dish_frequencies.items():
#         freq.append((frequency, dish))
#     return sorted(freq)


def get_similar_dishes(dish_id):
# return list of dishes that are most similar to <dish>
    key = 'similarities_item:' + str(dish_id)
    print key
    matches = model.r.lrange(key, 0, -1)
    print matches
    if matches == []:
        similar_dishes = []
    else:
        similar_dishes = []
        for item_id in matches:
            item_id = int(item_id)
            item = model.session.query(model.Item).get(item_id)
            similar_dishes.append(item)
    return similar_dishes


def get_total_dishes():
    count = model.session.query(model.Item).count()
    return count


def get_random_dish():
    count = get_total_dishes()
    num = randint(1, count)
    dish = model.session.query(model.Item).get(num)
    if dish == None:
        dish = get_random_dish()
    return dish


