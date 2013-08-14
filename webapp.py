#!/usr/bin/python

from flask import Flask, render_template, redirect, request
import model
import controller
import os, sys

sys.path.append(os.getcwd())
sys.path.append("../")
app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


@app.route("/")
def index():
    # generate counts for main chart of menus by decade
    decade_list = controller.counts_for_all_decades()
    menu_total = controller.get_total_menus()
    item_total = controller.get_total_dishes()
    restaurant_total = controller.get_total_restaurants()
    return render_template("index.html", decade_list=decade_list, 
                                         menu_total=menu_total,
                                         restaurant_total=restaurant_total,
                                         item_total=item_total)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/random/<selection>")
def get_random(selection):
    if selection == 'menu':
        menu = controller.get_random_menu()
        return redirect('../menu/' + str(menu.id))
    elif selection == 'restaurant':
        restaurant = controller.get_random_restaurant()
        return redirect('../restaurant/' + str(restaurant.id))
    else:
        item = controller.get_random_dish()
        return redirect('../item/' + str(item.id))


@app.route("/item/<int:item_id>")
def item_details(item_id):
    item = model.session.query(model.Item).get(item_id)
    menus = []    
    for i in item.menus:
        if i.menu != None:
            menus.append(i.menu)
    menus = sorted(menus, reverse=True)
    menu_count = len(menus)
    similarities = controller.get_similar_dishes(item_id)
    techniques = model.r.lrange(('item_techniques:' + str(item_id)), 0, -1)
    categories = model.r.lrange(('item_categories:' + str(item_id)), 0, -1)
    return render_template("item.html", item=item, 
                                        menus=menus,
                                        similarities=similarities,
                                        techniques=techniques,
                                        count=menu_count,
                                        categories=categories
                                        )


@app.route("/menu/<int:menu_id>")
def menu_details(menu_id):
    menu = model.session.query(model.Menu).get(menu_id)
    items = []
    for i in menu.items:
        items.append(i.item)
    item_count = len(items)
    other_restaurant_menus = []
    menus = menu.restaurant.menus
    # for j in menus:
    #     other_restaurant_menus.append(j)
    menu_count = len(menus)
    # similarities = controller.get_similar_menus(menu_id)
    return render_template("menu.html", menu=menu, 
                                        items=items, 
                                        menus=menus,
                                        item_count=item_count,
                                        # similarities=similarities,
                                        menu_count=menu_count)


@app.route("/restaurant/<int:restaurant_id>")
def restaurant_details(restaurant_id):
    restaurant = model.session.query(model.Restaurant).get(restaurant_id)
    menu_count = len(restaurant.menus)
    menus = sorted(restaurant.menus)
    print menus
    return render_template("restaurant.html", restaurant=restaurant,
                                              menus=menus, 
                                              count=menu_count)


@app.route("/technique/<technique>")
def technique_details(technique):
    dishes = controller.find_dishes_by_technique(technique)
    count = len(dishes)
    return render_template("technique.html", technique=technique,
                                             dishes=dishes,
                                             count=count)


@app.route("/category/<category>")
def category_details(category):
    dishes = controller.find_dishes_by_category(category)
    count = len(dishes)
    return render_template("category.html", category=category,
                                            dishes=dishes,
                                            count=count)



@app.route("/explore_techniques")
def explore_techniques():
    return render_template("explore_techniques.html")


@app.route('/explore_categories')
def explore_categories():
    return render_template("explore_categories.html")


@app.route('/decade_results/')
def decade_results():
    decade = str(request.args.get('decade'))
    return redirect('/decade/' + decade)


@app.route('/decade/<int:decade>')
def decade_display(decade):
    yearlist = controller.counts_for_all_years(decade)
    popular = controller.get_popular_dishes_decade(decade)
    print popular
    return render_template('decade.html', popular=popular,
                                          decade=decade,
                                          yearlist=yearlist)


@app.route('/year/<int:year>')
def year_display(year):
    menu_count = controller.count_menus_by_year(year)
    item_count = controller.total_dishes_per_year(year)
    popular = controller.get_popular_dishes_year(year)
    return render_template('year.html', year=year,
                                        menu_count=menu_count,
                                        item_count = item_count,
                                        popular = popular)


@app.route('/item_results')
def item_results():
    keyword = request.args.get('search')
    keyword_cap = keyword.capitalize()
    results = controller.find_dishes_by_keyword(keyword_cap)
    if results == False:
        results = ["No results found."]
    count = len(results)
    return render_template("item_results.html", keyword=keyword, 
                                                results=results,
                                                count=count)


@app.route("/restaurant_results")
def restaurant_results():
    keyword = request.args.get("search")
    results = controller.find_restaurant_by_name(keyword)
    if results == False:
        results = ["No results found."]
    count = len(results)
    print results
    return render_template("restaurant_results.html", keyword=keyword, 
                                                results=results,
                                                count=count)

if __name__ == "__main__":
    app.run(debug=True)  # turn off debug in production!


########

# error handlers (from Flask megatutorial):
#
# @app.errorhandler(404)
# def internal_error(error):
#     return render_template('404.html'), 404
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500

# http://blog.miguelgrinberg.com/post/
# the-flask-mega-tutorial-part-vii-unit-testing
