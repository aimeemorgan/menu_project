from app import model
import csv
import datetime


def load_menus_and_restaurants(session):
    with open('./ref_files/Menu.csv') as csvfile:
        menureader = csv.reader(csvfile, delimiter=",")
        rest_id = 1
        for row in menureader:  
            new_restaurant = model.Restaurant(name=row[13],
                                            location=row[5].title().strip(";"),
                                            id=rest_id)
            session.add(new_restaurant)
            session.commit()
            if row[12] != '':  # format date
                date_args = row[12].split('-')
                date = datetime.date((int(date_args[0])),
                                     (int(date_args[1])),
                                     (int(date_args[2])))
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
    with open('./ref_files/Dish.csv') as csvfile:
        itemreader = csv.reader(csvfile, delimiter=",")
        for row in itemreader:
            first_year = None  # format dates
            latest_year = None
            if row[5] != '0':  
                first_year = datetime.date(int(row[5]), 1, 1)
            if row[6] != '0':
                latest_year = datetime.date(int(row[6]), 1, 1)
            low_price = None
            high_price = None
            if row[7] != '':
                low_price=float(row[7])
            if row[8] != '':
                high_price=float(row[8])
            print row[1]
            new_item = model.Item(id=int(row[0]),
                                  description=row[1].strip("\"").title(),
                                  first_year=first_year,
                                  latest_year=latest_year,
                                  low_price=low_price,
                                  high_price=high_price)
            session.add(new_item)
            session.commit()


def main(session):
    load_menus_and_restaurants(session)
    load_items(session)


if __name__ == "__main__":
    s = model.session
    main(s)
