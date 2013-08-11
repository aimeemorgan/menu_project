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
    # generate counts for main map of menus by decade
    decade_list = controller.counts_for_all_decades()
    random_item = controller.get_random_dish()
    random_menu = controller.get_random_menu()
    random_restaurant = controller.get_random_restaurant()
    menu_total = controller.get_total_menus()
    item_total = controller.get_total_dishes()
    restaurant_total = controller.get_total_restaurants()
    return render_template("index.html", decade_list=decade_list, 
                                         random_item=random_item,
                                         random_menu=random_menu,
                                         random_restaurant=random_restaurant,
                                         menu_total=menu_total,
                                         restaurant_total=restaurant_total,
                                         item_total=item_total)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/item/<int:item_id>")
def item_details(item_id):
    item = model.session.query(model.Item).get(item_id)
    menus = []    
    for i in item.menus:
        if i.menu != None:
            menus.append(i.menu)
    menus = sorted(menus)
    menu_count = len(menus)
    # similarities = controller.get_similar_dishes(item_id)
    return render_template("item.html", item=item, 
                                        menus=menus,
                                        # similarities=similarities,
                                        count=menu_count
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
    for j in menus:
        other_restaurant_menus.append(j)
    menu_count = len(menus)
    # similarities = controller.get_similar_menus(menu_id)
    return render_template("menu.html", menu=menu, 
                                        items=items, 
                                        menus=menus,
                                        item_count=item_count,
                                        # similarities=similarities,
                                        menu_count=menu_count
                                        )


@app.route("/restaurant/<int:restaurant_id>")
def restaurant_details(restaurant_id):
    restaurant = model.session.query(model.Restaurant).get(restaurant_id)
    menu_count = len(restaurant.menus)
    return render_template("restaurant.html", restaurant=restaurant, count=menu_count)


@app.route("/technique/<int:technique_id>")
def technique_details(technique_id):
    technique = model.session.query(model.Technique).get(technique_id)
    return render_template("technique.html", technique=technique)


@app.route("/explore_techniques")
def explore_techniques():
    return render_template("explore_techniques.html")


@app.route("/explore_categories")
def explore_categories():
    return render_template("explore_categories.html")


@app.route("/explore_decades")
def explore_decades():
    return render_template("explore_decades.html")


@app.route("/item_results")
def item_results():
    keyword = request.args.get("search")
    results = controller.find_dishes_by_keyword(keyword)
    if results == False:
        results = ["No results found."]
    count = len(results)
    return render_template("item_results.html", keyword=keyword, 
                                                results=results,
                                                count=count)


@app.route("/restaurant_results")
def restaurant_results():
    keyword = request.args.get("search")
    results = controller.find_dishes_by_keyword(keyword)
    if results == False:
        results = ["No results found."]
    count = len(results)
    return render_template("item_results.html", keyword=keyword, 
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
