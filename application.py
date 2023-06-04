import random
import datetime

from faker import Faker

from data import film_categories, film_languages, countries, can_cities, us_cities
from session import session
from models import Base, Film, Category, Language, Country, Actor, FilmCategory, City,\
    Address, Store, Staff, Payment, Customer, Inventory, Rental, FilmActor


def add_categories():
    for i in film_categories:
        category = Category(name=i)

        session.add(category)
        session.commit()


def add_languages():
    for i in film_languages:
        language = Language(name=i)

        session.add(language)
        session.commit()


def add_countries():
    for i in countries:
        country = Country(name=i)

        session.add(country)
        session.commit()


def add_actors(count=10):
    fake = Faker()
    actors = [Actor(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
        for _ in range(count)
    ]
    session.add_all(actors)
    session.commit()


def add_film(count=10):
    fake = Faker()
    films = [Film(
        title=fake.word(),
        description=fake.sentence(),
        release_year=fake.random_int(min=1980, max=2019),
        language_id=random.choice([r.language_id for r in session.query(Language).all()]),
        rental_duration=fake.random_int(min=1, max=10),
        rental_rate=round(random.uniform(1.10, 2.00), 2),
        length=fake.random_int(min=90, max=210),
        replacement_cost=fake.random_int(min=50, max=100),
        rating=fake.random_int(min=1, max=10),
        special_features=fake.sentence(),
        fulltext=fake.sentence()
    )
        for _ in range(count)
    ]

    session.add_all(films)
    session.commit()


def assign_films_to_categories():
    films = [r.id for r in session.query(Film).all()]
    categories = [r.id for r in session.query(Category).all()]
    for i in films:
        film_category = FilmCategory(
            film_id=i,
            category_id=random.choice(categories)
        )
        session.add(film_category)
        session.commit()


def add_cities():
    for i in can_cities:
        city = City(
            city=i,
            country_id= session.query(Country.coutry_id).filer_by(Country.country == "Canada")
        )
        session.add(city)
        session.commit()
    for i in us_cities:
        city = City(
            city=i,
            country_id= session.query(Country.coutry_id).filer_by(Country.country == "USA")
        )
        session.add(city)
        session.commit()



if __name__ == '__main__':
    print("Creating database tables...")
    Base.metadata.create_all()

    print("Adding categories...")
    add_categories()
    print("Adding languages...")
    add_languages()
    print("Adding countries...")
    add_countries()
    print("Adding actors...")
    add_actors()
    print("Adding films...")
    add_film()
    print("Assigning films to categories...")
    assign_films_to_categories()
    print("Adding cities...")
    add_cities()
