
import model
import csv
import datetime


def load_menus_and_restaurants(session):
    with open('./ref_docs/Menu.csv') as csvfile:
        menureader = csv.reader(csvfile, delimiter=",")
        for row in menureader:  # format date
            #     title = row[1]
            #     title = title.decode("latin-1")
            #     r_date = row[2].split("-")
            #     months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
            #     r_date_datetime = datetime.date(int(r_date[2]), int(months[r_date[1]]), int(r_date[0]))
            new_menu = model.Menu(id=int(row[0]), date=row[11],
                                  currency=row[14], occasion=row[7],
                                  sponsor=row[2])
            session.add(new_menu)
            new_restaurant = model.Restaurant(name=row[13], location=row[5])
            session.add(new_restaurant)
            session.commit()


def load_items(session):
    with open('./ref_docs/Dish.csv') as csvfile:
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:  # put date for first and latest years in correct format
            #     title = row[1]
            #     title = title.decode("latin-1")
            #     r_date = row[2].split("-")
            #     months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
            #     r_date_datetime = datetime.date(int(r_date[2]), int(months[r_date[1]]), int(r_date[0]))
            new_item = model.Item(id=row[0], description=row[x], 
                                  first_year=row[x], latest_year=row[x],
                                  low_price=float(row[x]),
                                  high_price=float(row[x]))
            session.add(new_item)
            session.commit()


def load_menusitems(session):
    pass

def load restaurantsmenus(session):
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_menus_and_restaurants(session)
    load_items(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)