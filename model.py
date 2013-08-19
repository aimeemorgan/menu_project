import redis
import locale

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from titlecase import titlecase

engine = create_engine('postgresql+psycopg2://alm:password@localhost/menus2')
# for heroku deploy, will need to modify this to point to DATABASE_URL.

session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush = False))

r = redis.StrictRedis(host='localhost', port=6379, db=0)

Base = declarative_base()
Base.query = session.query_property()


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    location = Column(String(256))

    menus = relationship("Menu", backref=backref("restaurant"))


    def __repr__(self):
        name = self.name
        location = self.location
        return '<Restaurant: %s. Location: %s>' % (name, location)

    def get_menus_date_sorted(self):
        menus = self.menus
        sortlist = []
        dateless = []
        for menu in menus:
            if menu != None:
                if menu.date != None:
                    sortlist.append((menu.date, menu))
                else:
                    dateless.append(menu)
        results = sorted(sortlist)
        for menu in dateless:
            results.append(('undated', menu))
        return results

    @property
    def lastdate(self):
        menus = self.get_menus_date_sorted()
        for result in menus:
            if result[0] == 'undated':
                menus.remove(result)
            for i in range (0, len(menus)):
                menu = menus[i][1]
                if menu.date.year > 1850:
                    lastdate = menu.datestring
                    return lastdate
        return self.firstdate

    @property
    def firstdate(self):
        menus = self.get_menus_date_sorted()
        for result in menus:
            if result[0] == 'undated':
                menus.remove(result)
            for i in range ((len(menus)-1), -1, -1):
                menu = menus[i][1]
                if menu.date.year < 2013:
                    firstdate = menu.datestring
                    return firstdate
        return None


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
        return '<%s, %s>' % (self.date,
                            self.restaurant.name)

    def get_items(self):
        items = []
        for item in self.items:
            items.append(item.item)
        return items

    def count_items(self):
        return len(self.items)


    @property
    def datestring(self):
        months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        month = months[self.date.month]
        day = str(self.date.day)
        year = str(self.date.year)
        datestring = "date unknown"
        if self.date.day:
            datestring = month + ' ' + day + ',' + ' ' + year
        elif self.date.month:
            datestring = month + ' ' + year
        elif self.date.year:
            datestring = year
        return datestring


class Item(Base): 
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    # first_year = Column(DateTime, nullable=True)
    # latest_year = Column(DateTime, nullable=True)
    # low_price = Column(Float, nullable=True)
    # high_price = Column(Float, nullable=True)
    # category = Column(String, nullable=True)

    menus = relationship("MenuItem", backref=backref("items"))

    def __repr__(self):
        description = self.description.encode
        return '<Item: %s>' % description

    def get_menus(self):
        menus = []
        for menu in self.menus:
            menus.append(menu.menu)
        return menus

    def get_menus_date_sorted(self):
        menus = self.get_menus()
        sortlist = []
        dateless = []
        for menu in menus:
            if menu != None:
                if menu.date != None:
                    sortlist.append((menu.date, menu))
                else:
                    dateless.append(menu)
        results = sorted(sortlist, reverse=True)
        for menu in dateless:
            results.append(('undated', menu))
        return results

    def count_menus(self):
        return len(self.menus)

    def get_restaurants(self):
        restaurants = []
        for menu in self.menus:
            restaurants.append(menu.menu.restaurant)
        return restaurants

    def count_restaurants(self):
        return len(self.get_restaurants())

    @property
    def prices(self):
        locale.setlocale( locale.LC_ALL, '' )
        prices = []
        menus = self.menus
        for menu in menus:
            if type(menu.price) == float:
                price = locale.currency(menu.price)
                prices.append(price)
        prices = sorted(prices)
        return prices

    @property
    def lowprice(self):
        locale.setlocale( locale.LC_ALL, '' )
        prices = self.prices
        for i in range(0, len(prices)):
            if prices[i]:
                if prices[i] != 'unknown':
                    return prices[i]
        return "unknown"

    @property
    def highprice(self):
        locale.setlocale( locale.LC_ALL, '' )
        prices = self.prices
        for i in range((len(prices)-1), -1, -1):
            if prices[i]:
                if prices[i] != 'unknown':
                    return prices[i]
        return self.lowprice

    @property
    def name(self):
        name = titlecase(self.description)
        return name

    @property
    def firstdate(self):
        menus = self.get_menus_date_sorted()
        for result in menus:
            if result[0] == 'undated':
                menus.remove(result)
        for i in range ((len(menus)-1), -1, -1):
            menu = menus[i][1]
            if menu.date.year > 1850:
                firstdate = menu.datestring
                return firstdate
        return self.lastdate

    @property
    def lastdate(self):
        menus = self.get_menus_date_sorted()
        for result in menus:
            if result[0] == 'undated':
                menus.remove(result)
        for i in range (0, len(menus)):
            menu = menus[i][1]
            if menu.date.year < 2013:
                lastdate = menu.datestring
                return lastdate
        return None


class MenuItem(Base):
    __tablename__ = "menuitems"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Float, nullable=True)

    item = relationship("Item", backref=backref("menuitem"))
    menu = relationship("Menu", backref=backref("menuitem"))
    
    @property
    def stringprice(self):
        locale.setlocale( locale.LC_ALL, '' )
        if self.price != None:
            stringprice = locale.currency(self.price)
        else:
            stringprice = "unknown"
        return stringprice

def main():
    pass

if __name__ == "__main__":
    main()
