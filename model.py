from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('postgresql+psycopg2://alm:password@localhost/nyplmenus')
# for heroku deploy, will need to modify this to point to DATABASE_URL.

session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here 
# restaurant = session.query(Restaurant).get(12882)

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    location = Column(String(256))

    menus = relationship("Menu", backref=backref("restaurant"))

    def __repr__(self):
        return '<Restaurant: %s. Location: %s>' % (self.name, self.location)

    def show_menus(self):
        print "Menus from %s:" % (self.name)
        for menu in self.menus:
            print menu.date

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    currency = Column(String, nullable=True)
    occasion = Column(String, nullable=True)
    sponsor = Column(String)

    items = relationship("MenuItem", backref=backref("menus"))

    def __repr__(self):
        return '<Menu: %s, %s>' % (self.restaurant.name, self.date)

    def show_items(self):
        print  "Menu: %s, %s:" % (self.restaurant.name, self.date)
        for item in self.items:
            print item.item.description

    # menu count by year/decade?
    # menu list by year/decade?

class Item(Base): 
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    first_year = Column(DateTime, nullable=True)
    latest_year = Column(DateTime, nullable=True)
    low_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)

    menus = relationship("MenuItem", backref=backref("items"))

    def __repr__(self):
        return '<Item: %s>' % (self.description)


    def show_menus(self):
        print "Menus on which %s appears:" % (self.description)
        for menu in item.menus:
            print "%s, %s" % (menu.menu.restaurant.name, menu.menu.date)


    def show_restaurants(self):
        print "Restaurants which serve %s:" % (self.description)
        for menu in item.menus:
            print menu.menu.restaurant.name


class MenuItem(Base):
    __tablename__ = "menuitems"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    price = Column(Float, nullable=True)

    item = relationship("Item", backref=backref("menuitem"))
    menu = relationship("Menu", backref=backref("menuitem"))


### End class declarations

def main():
    pass

if __name__ == "__main__":
    main()
