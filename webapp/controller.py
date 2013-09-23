import model
import helper
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


@app.route("/")
def index():
    # generate counts for main chart of menus by decade
    decade_list = helper.counts_for_all_decades()
    menu_total = helper.get_total_menus()
    item_total = helper.get_total_dishes()
    restaurant_total = helper.get_total_restaurants()
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
        menu = helper.get_random_menu()
        return redirect('../menu/' + str(menu.id))
    elif selection == 'restaurant':
        restaurant = helper.get_random_restaurant()
        return redirect('../restaurant/' + str(restaurant.id))
    else:
        item = helper.get_random_dish()
        return redirect('../item/' + str(item.id))


@app.route("/item/<int:item_id>")
def item_details(item_id):
    item = model.session.query(model.Item).get(item_id)
    menus = item.get_menus_date_sorted()
    menu_count = len(menus)
    similarities = helper.get_similar_dishes(item_id)
    if similarities == []:
        similarities = ['no similar items found']
    techniques = helper.get_techniques_for_dish(item_id)
    categories = helper.get_categories_for_dish(item_id)
    return render_template("item.html", item=item, 
                                        menus=menus,
                                        similarities=similarities,
                                        techniques=techniques,
                                        count=menu_count,
                                        categories=categories)


@app.route("/menu/<int:menu_id>")
def menu_details(menu_id):
    menu = model.session.query(model.Menu).get(menu_id)
    items = []
    for i in menu.items:
        items.append((i.item, i.stringprice))
    item_count = len(items)
    menus = menu.restaurant.menus
    menu_count = len(menus)
    # similarities = helper.get_similar_menus(menu_id)
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
    menus = restaurant.get_menus_date_sorted()
    return render_template("restaurant.html", restaurant=restaurant,
                                              menus=menus, 
                                              count=menu_count)


@app.route("/technique/<technique>")
def technique_details(technique):
    dishes = helper.find_dishes_by_technique(technique, limit=50)
    count = len(dishes)
    return render_template("technique.html", technique=technique,
                                             dishes=dishes,
                                             count=count)


@app.route("/category/<category>")
def category_details(category):
    dishes = helper.find_dishes_by_category(category, limit=50)
    count = len(dishes)
    return render_template("category.html", category=category,
                                            dishes=dishes,
                                            count=count)



@app.route("/explore_techniques")
def explore_techniques():
    results = helper.find_dishes_select_techniques()
    return render_template("explore_techniques.html", results=results)


@app.route('/explore_categories')
def explore_categories():
    results = helper.find_dishes_select_categories()
    return render_template("explore_categories.html", results=results)


@app.route('/decade_results/')
def decade_results():
    decade = str(request.args.get('decade'))
    return redirect('/decade/' + decade)


@app.route('/decade/<int:decade>')
def decade_display(decade):
    yearlist = helper.counts_for_all_years(decade)
    popular = helper.get_popular_dishes_decade(decade)
    return render_template('decade.html', popular=popular,
                                          decade=decade,
                                          yearlist=yearlist)


@app.route('/year/<int:year>')
def year_display(year):
    menu_count = helper.count_menus_by_year(year)
    item_count = helper.get_item_count_by_year(year)
    popular = helper.get_popular_dishes_year(year)
    menus = helper.find_menus_by_year(year, limit=50)
    return render_template('year.html', year=year,
                                        menu_count=menu_count,
                                        item_count = item_count,
                                        menus=menus,
                                        popular = popular)


@app.route('/item_results')
def item_results():
    keyword = request.args.get('search')
    keyword_cap = keyword.capitalize()
    results = helper.find_dishes_by_keyword(keyword_cap)
    count = len(results)
    return render_template("item_results.html", keyword=keyword, 
                                                results=results,
                                                count=count)


@app.route("/restaurant_results")
def restaurant_results():
    keyword = request.args.get('search')
    results = helper.find_restaurant_by_name(keyword)
    if results == False:
        results = ['No results found']
    count = len(results)
    return render_template("restaurant_results.html", keyword=keyword, 
                                                results=results,
                                                count=count)




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
