"""
Seeder de l'application
(génère un jeu d'essai aléatoire)
"""

from services import TravelService, CityService
from models import City, Travel, Accomodation, Transport, Session
from faker import Factory
import random
import datetime


class Seeder:
    """
    Seeder
    """

    def __init__(self, number_of_cities=60, number_of_travels=30):
        """
        Constructor
        :param session: Session
        :param number_of_cities: integer
        :param number_of_travels: integer
        :return: void
        """
        self.session = Session()
        self.travel_service = TravelService()
        self.city_service = CityService()
        self.fake = Factory.create()
        self.number_of_cities = number_of_cities
        self.number_of_travels = number_of_travels

    def run(self):
        """
        Point d'entrée
        :return: void
        """
        self.seed_cities(self.number_of_cities)
        self.seed_travels(self.number_of_travels)
        self.session.close()

    def seed_cities(self, number):
        """
        Crée des enregistrements aléatoires dans la table des villes
        :param number: nombre de villes
        :return: void
        """
        for i in range(0, number):
            city = City()
            city.name = self.fake.city()
            city.country = self.fake.country()
            city.is_capital = self.fake.pybool()
            self.city_service.save(city)

        capitals = self.city_service.all_capitals()
        non_capitals = self.city_service.all_non_capitals()

        for city in non_capitals:
            city.capital_id = random.choice(capitals).id
            self.city_service.save(city)

    def seed_travels(self, number):
        """
        Crée des enregistrements aléatoires dans la table des voyages
        :param number: nombre de voyages
        :return: void
        """
        cities = self.city_service.all()

        for i in range(0, number):
            travel = Travel()
            travel.start = self.fake.date_time_this_year(before_now=True, after_now=False)
            travel.end = travel.start + datetime.timedelta(days=random.randrange(1, 10, 1))
            travel.review = self.fake.text(max_nb_chars=200)
            travel.city_id = random.choice(cities).id

            for j in range(0, 3):
                transport = Transport()
                transport.type = random.choice(['Train', 'Avion', 'Voiture', 'Bateau', 'Bus'])
                transport.price = random.randrange(10, 150, 5)
                transport.duration = random.randrange(1, 24, 1)
                travel.transports.append(transport)

            for k in range(0, 3):
                accomodation = Accomodation()
                accomodation.name = self.fake.company()
                accomodation.type = random.choice(['Camping', 'Hôtel', 'Gîte', 'Appartement'])
                accomodation.price = random.randrange(50, 500, 10)
                travel.accomodations.append(accomodation)

            self.travel_service.save(travel)


if __name__ == '__main__':
    seeder = Seeder()
    seeder.run()