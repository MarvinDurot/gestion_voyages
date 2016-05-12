"""
Seeder de l'application
(génère un jeu d'essai aléatoire)
"""

from facades import TravelFacade, CityFacade
from models import City, Travel, Accomodation, Transport
from faker import Factory
import random
import datetime

# Création du générateur
fake = Factory.create()


def seed_cities(number):
    """
    Crée des enregistrements aléatoires dans la table des villes
    :param number: nombre de villes
    :return:
    """
    for i in range(0, number):
        city = City()
        city.name = fake.city()
        city.country = fake.country()
        city.is_capital = fake.pybool()
        CityFacade.save(city)

    capitals = CityFacade.all_capitals()
    non_capitals = CityFacade.all_non_capitals()

    for city in non_capitals:
        city.capital_id = random.choice(capitals).id
        CityFacade.save(city)


def seed_travels(number):
    """
    Crée des enregistrements aléatoires dans la table des voyages
    :param number: nombre de voyages
    :return:
    """
    cities = CityFacade.all()

    for i in range(0, number):
        travel = Travel()
        travel.start = fake.date_time_this_year(before_now=True, after_now=False)
        travel.end = travel.start + datetime.timedelta(days=random.randrange(1, 10, 1))
        travel.review = fake.text(max_nb_chars=200)
        travel.city_id = random.choice(cities).id

        for j in range(0, 3):
            transport = Transport()
            transport.type = random.choice(['Train', 'Avion', 'Voiture', 'Bateau', 'Bus'])
            transport.price = random.randrange(10, 150, 5)
            transport.duration = random.randrange(1, 24, 1)
            travel.transports.append(transport)

        for k in range(0, 3):
            accomodation = Accomodation()
            accomodation.name = fake.company()
            accomodation.type = random.choice(['Camping', 'Hôtel', 'Gîte', 'Appartement'])
            accomodation.price = random.randrange(50, 500, 10)
            travel.accomodations.append(accomodation)

        TravelFacade.save(travel)


if __name__ == '__main__':
    # On remplit les tables de la base
    seed_cities(30)
    seed_travels(20)
