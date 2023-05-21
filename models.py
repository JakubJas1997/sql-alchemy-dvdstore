import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from session import engine

Base = declarative_base(bind=engine)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    film_category = relationship('FilmCategory')

    def __repr__(self):
        return f"Category name: {self.name}"


class FilmCategory(Base):
    __tablename__ = 'film_category'

    film_id = Column(Integer,
                     ForeignKey('film.id'),
                     nullable=False)
    category_id = Column(Integer,
                         ForeignKey('category.id'),
                         nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    release_year = Column(DateTime)
    language_id = Column(Integer,
                         ForeignKey('language.id'),
                         nullable=False)
    rental_duration = Column(Integer)
    rental_rate = Column(Integer)
    length = Column(Integer)
    replacement_cost = Column(Integer)
    rating = Column(Integer)
    last_updated = Column(DateTime, nullabe=False, default=datetime.datetime.now)
    special_features = Column(Text)
    fulltext = Column(Text)

    film_category = relationship('FilmCategory')

    def __repr__(self):
        return f"Film title: {self.title}"


class Language(Base):
    __tablename__ = 'language'

    language_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    last_updated = Column(DateTime, nullable=False, default=datetime.datetime.now)

    film = relationship('Film')

    def __repr__(self):
        return f"Language: {self.name}"

