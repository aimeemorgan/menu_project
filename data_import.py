import model
import csv
import datetime


def load_menus_and_restaurants(session):
    with open('./ref_docs/menu_test') as csvfile:
        menureader = csv.reader(csvfile, delimiter=",")
        rest_id = 1
        for row in menureader:  # format date
            new_restaurant = model.Restaurant(name=row[13],
                                            location=row[5].title().strip(";"),
                                            id=rest_id)
            session.add(new_restaurant)
            session.commit()
            if row[12] != '':
                date_args = row[12].split('-')
                date = datetime.date(int(date_args[0]),
                                     int(date_args[1]),
                                     int(date_args[2]))
            else:
                date = None
            new_menu = model.Menu(id=int(row[0]),
                                  date=date,
                                  currency=row[14],
                                  occasion=row[7].strip(";").title(),
                                  sponsor=row[2].title(),
                                  restaurant_id=rest_id)
            session.add(new_menu)
            session.commit()
            rest_id += 1


def load_items(session):
    with open('./ref_docs/dishes_test.csv') as csvfile:
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:
            new_item = model.Item(id=int(row[0]),
                                  description=row[1].strip("\"").title(),
                                  first_year=datetime.date(int(row[5]), 1, 1),
                                  latest_year=datetime.date(int(row[6]), 1, 1),
                                  low_price=float(row[7]),
                                  high_price=float(row[8]))
            session.add(new_item)
            session.commit()


def load_menuitems(session):
    ##### read menupages csv and create a dictionary w menu page IDs as keys, and menu IDs as values
    #### them get penu page IDs while reading the menuitems csv below, use it to look up the menu ID
    ### and feed it into the database as a argument below

    # build menu_page_id to menu_id dictionary
    with open ('./ref_docs/MenuPage.csv') as csvfile:
        menu_ids = {}
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:
            menu_ids[row[0]] = menu_ids[1]

    with open('./ref_docs/menuitem_test.csv') as csvfile:
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:
            menu_id = menu_ids[row[1]]
            new_menuitem = model.menuitems(id=int(row[0]),
                                  item_id=row[4],
                                  menu_id=menu_id,
                                  price=float(row[2]))
            session.add(new_menuitem)
            session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    #load_menus_and_restaurants(session)
    load_items(session)

if __name__ == "__main__":
    s = model.session
    main(s)