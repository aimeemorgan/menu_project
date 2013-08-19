# Menu Scout

[Hackbright Academy] (http://www.hackbrightacademy.com) final project using the New York Public Library's "What's on the Menu?" dataset (http://menus.nypl.org/). 
More information at http://aimeecodes.blogspot.com/2013/07/project-plan-reveal.html.

Technologies: Python, Postgresql, Redis, NLTK, Flask, SQLAlchemy, Bootstrap.

## Summary

Menu Scout: a web app that allows users to explore 150 years of culinary history via data from the New York Public Library's "What's on the Menu?" project. The short version: NYPL is digitizing their collection of 45,000+ historical restaurant menus, putting the scans on their web site, and asking the food-loving public to help provide text transcriptions. All the transcriptions completed to date are available for download. It's a fascinating, but messy, data set. On the back end, Menu Scout uses data analysis and natural language processing techniques to provide users with new ways to search and browse this unique historical resource.

## Import Tools

(For importing data from NYPL's CSV files)

data_import.py: Imports information on menus, items, and restaurants

menuitems_import.py: For creating links between menus and items. Generates a CSV file for copying into postgres database.


## Data Processing Tools

(Run in interactive mode to generate and persist information about the dataset.)

restaurant_dedup.py: Cleans up Restaurants database table by identifying and merging duplicate entries.
 
data_processing.py: Various data processing functions. Requires helper.py and model.py.

all_pairs.py: Implementation of basic all pairs matching algorithm for finding similar items / similar menus, as
described by Bayardo et. al., 2007 (see http://bayardo.org/ps/www2007.pdf for detailed description).

classifier.py: Tool for assigning categories to dishes.

lexicon.py: Sets up lexicons used by the classifier. Lexicon lists are stored as text files in /lexicons.

model.py: Defines classes for restaurants, 


## Front End

controller.py: Handlers for web requests. Requires model.py and helper.py.

helper.py: Functions for querying the database and returning results to controller.py.

templates/: The views! Jinja templates for use by controller.py handlers.
