import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from session import engine

Base = declarative_base(bind=engine)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    film_category = relationship('FilmCategory', cascade='all,delete,delete-orphan')

    def __repr__(self):
        return f"Category name: {self.name}"


class FilmCategory(Base):
    __tablename__ = 'film_category'

    film_id = Column(Integer,
                     ForeignKey('film.id'),
                     primary_key=True,
                     nullable=False)
    category_id = Column(Integer,
                         ForeignKey('category.id'),
                         primary_key=True,
                         nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    release_year = Column(DateTime)
    language_id = Column(Integer,
                         ForeignKey('language.language_id'),
                         nullable=False)
    rental_duration = Column(Integer)
    rental_rate = Column(Integer)
    length = Column(Integer)
    replacement_cost = Column(Integer)
    rating = Column(Integer)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)
    special_features = Column(Text)
    fulltext = Column(Text)

    film_category = relationship('FilmCategory', cascade='all,delete,delete-orphan')
    film_actor = relationship('FilmActor')
    inventory = relationship('Inventory')

    def __repr__(self):
        return f"Film title: {self.title}"


class Language(Base):
    __tablename__ = 'language'

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    film = relationship('Film')

    def __repr__(self):
        return f"Language: {self.name}"


class Actor(Base):
    __tablename__ = 'actor'

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    film_actor = relationship('FilmActor')

    def __repr__(self):
        return f"Actor: {self.first_name} {self.last_name}"


class FilmActor(Base):
    __tablename__ = 'film_actor'

    actor_id = Column(Integer,
                      ForeignKey('actor.actor_id'),
                      primary_key=True,
                      )
    film_id = Column(Integer,
                     ForeignKey('film.id'),
                     primary_key=True,
                     )
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    film_id = Column(Integer,
                     ForeignKey('film.id'),
                     nullable=False,
                     primary_key=True)
    store_id = Column(Integer)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Rental(Base):
    __tablename__ = 'rental'

    rental_id = Column(Integer, primary_key=True, autoincrement=True)
    rental_date = Column(DateTime, nullable=False)
    inventory_id = Column(Integer,
                          ForeignKey('inventory.inventory_id'),
                          nullable=False,
                          primary_key=True)
    customer_id = Column(Integer,
                         ForeignKey('customer.customer_id'),
                         nullable=False, )
    return_date = Column(DateTime, nullable=False)
    staff_id = Column(Integer,
                      ForeignKey('staff.staff_id'),
                      nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    inventory = relationship('Inventory')
    staff = relationship('Staff')


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer,
                      ForeignKey('store.store_id'),
                      nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    address_id = Column(Integer,
                        ForeignKey('address.address_id'),
                        nullable=False,
                        primary_key=True)
    is_active = Column(Boolean, nullable=False, default=True)
    create_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'), nullable=False)

    def __repr__(self):
        return f"Customer: {self.first_name}, {self.last_name}, {self.email}"


class Staff(Base):
    __tablename__ = 'staff'

    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address_id = Column(Integer,
                        ForeignKey('address.address_id'),
                        nullable=False,
                        primary_key=True)
    store_id = Column(Integer,
                      ForeignKey('store.store_id'),
                      nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)
    picture = Column(String(50), nullable=False)

    address = relationship('Address')

    def __repr__(self):
        return f"Staff: {self.first_name}, {self.last_name}, {self.username}"


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer,
                         ForeignKey('customer.customer_id'),
                         nullable=False,
                         primary_key=True)
    staff_id = Column(Integer,
                      ForeignKey('staff.staff_id'),
                      nullable=False,
                      primary_key=True)
    rental_id = Column(Integer,
                       ForeignKey('rental.rental_id'),
                       nullable=False,
                       primary_key=True)
    amount = Column(Integer, nullable=False)
    payment_date = Column(DateTime, nullable=False)

    rental = relationship('Rental')
    customer = relationship('Customer')
    staff = relationship('Staff')

    def __repr__(self):
        return f"Payment: {self.payment_id},{self.amount}"


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(50), nullable=False)
    address2 = Column(String(50), nullable=False, unique=True)
    district = Column(String(50), nullable=False)
    city_id = Column(Integer,
                     ForeignKey('city.city_id'),
                     nullable=False,
                     primary_key=True)
    postal_code = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)

    city = relationship('City')

    def __repr__(self):
        return f"Address: {self.address}, {self.address2}, {self.district}"


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(50), nullable=False, unique=True)
    country_id = Column(Integer,
                        ForeignKey('country.country_id'),
                        nullable=False,
                        primary_key=True)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)

    country = relationship('Country')

    def __repr__(self):
        return f"City: {self.city}"


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50), nullable=False, unique=True)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)

    def __repr__(self):
        return f"Country: {self.country}"

class Store(Base):
    __tablename__ ='store'

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    manager_staff_id = Column(Integer,
                              ForeignKey('staff.staff_id'),
                              nullable=False,)
    address_id = Column(Integer,
                        ForeignKey('address.address_id'),
                        nullable=False,
                        primary_key=True)
    last_update = Column(DateTime, nullable=False, default=datetime.datetime.now)

    address = relationship('Address')




Base.metadata.create_all(engine)
