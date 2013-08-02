#!/usr/bin/python

from flask import Flask, render_template, redirect, request
import model
import controller

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    model.session.remove()


@app.route("/")
def index():
	# generate counts for main map of menus by decade
	decade_list = controller.counts_for_all_decades
    return render_template("index.html" counts=decade_list)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dish")
def dish():
	return render_template("dish.html")


@app.route("/menu")
def menu():
	return render_template("menu.html")

app
@.route("/restaurant")
def restaurant():
	return render_template("restaurant.html")


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
