from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///ratings.db", echo=False) # replace w postgres connection info
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here 


class Menu(Base):  # menus
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True)
    currency = Column(String(32), nullable=True)
    occasion = Column(String(256), nullable=True)
    sponsor = Column(String(256))

    # rater = relationship("User", backref=backref("ratings", order_by=id))


class Restaurant(Base):  # restaurants
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    location = Column(String(256))

    menus = relationship("Menu,", backref=backref("menus"))
    # movie_ratings = relationship("Rating", backref=backref("users"))


class Item(Base):  # items
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    first_year = Column(DateTime, nullable=True)
    latest_year = Column(DateTime, nullable=True)
    low_price = Column(Number, nullable=True)
    high_price = Column(Float, nullable=True)

    # # use rating class as association object
    # ratings = relationship("Rating", backref="movies")



### End class declarations

def main():
    pass

if __name__ == "__main__":
    main()
