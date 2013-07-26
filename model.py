from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('postgresql+psycopg2://alm:password@localhost/nyplmenus')

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
        return '<Retsaurant: %s>' % (self.name)

    # def show_menus(self):

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

    # def show_items(self):

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

    # def show_menus(self):
    # def show_restaurants(self):


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
