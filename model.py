from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('postgresql+psycopg2://alm:password@localhost/menus')
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
    similarities = relationship("RestaurantSimilarity", backref=backref("restaurants"))

    def __repr__(self):
        name = self.name.encode('utf-8')
        location = self.location.encode('utf-8')
        return '<Restaurant: %s. Location: %s>' % (name, location)

    def get_menus_date_sorted(self):
        return sorted(self.menus)

    def earliest_menu_date(self):
        sorted = self.get_menus_date_sorted
        return sorted[0].date

    def latest_menu_date(self):
        sorted = self.get_menus_date_sorted
        return sorted[-1].date


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    currency = Column(String, nullable=True)
    occasion = Column(String, nullable=True)
    sponsor = Column(String)

    items = relationship("MenuItem", backref=backref("menus"))
    similarities = relationship("MenuSimilarity", backref=backref("menus"))


    def __repr__(self):
        return '<Menu: %s, %s>' % (self.date, self.restaurant.name)

    def get_items(self):
        items = []
        for item in self.items:
            items.append(item.item)
        return items

    def count_items(self):
        return len(self.items)


class Item(Base): 
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    first_year = Column(DateTime, nullable=True)
    latest_year = Column(DateTime, nullable=True)
    low_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    category = Column(Integer, ForeignKey('categories.id'), nullable=True)

    menus = relationship("MenuItem", backref=backref("items"))
    techniques = relationship("ItemTechnique", backref=backref("items"))
    ingredients = relationship("ItemIngredient", backref=backref("items"))
    similarities = relationship("ItemSimilarity", backref=backref("items"))


    def __repr__(self):
        description = self.description.encode('utf-8')
        return '<Item: %s>' % description

    def get_menus(self):
        menus = []
        for menu in self.menus:
            menus.append(menu.menu)
        return menus

    def count_menus(self):
        return len(self.menus)

    def get_restaurants(self):
        restaurants = []
        for menu in self.menus:
            restaurants.append(menu.menu.restaurant)
        return restaurants

    def count_restaurants(self):
        return len(self.get_restaurants())


    def get_ingredients(self):
        ingredients = []
        for ingredient in self.ingredients:
            ingredients.append(ingredient.menu.restaurant)
        return ingredients


class Technique(Base):
    __tablename__ = "techniques"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    items = relationship("ItemTechnique", backref=backref("techniques"))


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    items = relationship("Item", backref=backref("categories"))


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    items = relationship("ItemIngredient", backref=backref("ingredients"))


class ItemIngredient(Base):
    __tablename__ = "itemingredients"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    price = Column(Float, nullable=True)

    item = relationship("Item", backref=backref("itemingredient"))
    ingredient = relationship("Ingredient", backref=backref("itemingredient"))


class MenuItem(Base):
    __tablename__ = "menuitems"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Float, nullable=True)

    item = relationship("Item", backref=backref("menuitem"))
    menu = relationship("Menu", backref=backref("menuitem"))


class ItemTechnique(Base):
    __tablename__ = "itemtechniques"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    technique_id = Column(Integer, ForeignKey('techniques.id'), nullable=False)
  
    item = relationship("Item", backref=backref("itemtechniques"))
    technique = relationship("Technique", backref=backref("itemtechniques"))
    

class ItemSimilarity(Base):
    __tablename__ = "itemsimilarities"

    id = Column(Integer, primary_key=True)
    item_id_1 = Column(Integer, ForeignKey('items.id'), nullable=False)
    item_id_2 = Column(Integer, ForeignKey('items.id'), nullable=False)
    score = Column(Float, nullable=False)

    item = relationship("Item", backref=backref("similarities"))
#   this setup will result in each relationship being recorded twice -- better way?


class RestaurantSimilarity(Base):
    __tablename__ = "restaurantsimilarities"

    id = Column(Integer, primary_key=True)
    restaurant_id_1 = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    restaurant_id_2 = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    score = Column(Float, nullable=False)

    restaurant = relationship("Restaurant", backref=backref("similarities"))


class MenuSimilarity(Base):
    __tablename__ = "menusimilarities"

    id = Column(Integer, primary_key=True)
    menu_id_1 = Column(Integer, ForeignKey('menus.id'), nullable=False)
    menu_id_2 = Column(Integer, ForeignKey('menus.id'), nullable=False)
    score = Column(Float, nullable=False)

    menu = relationship("Menu", backref=backref("similarities"))

### End class declarations


def main():
    pass

if __name__ == "__main__":
    main()
