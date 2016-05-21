"""
Services de l'application
"""

from models import Travel, Transport, Accomodation, City, Session
import datetime


class GenericService:
    """
    Service générique permettant de manipuler
    les modèles en base plus simplement.
    """
    __modelClass__ = None

    def __init__(self):
        """
        Constructeur
        :return:
        """
        self.session = None

    def newSession(self):
        """
        Renouvelle la session du service
        :return:
        """
        if self.session is not None:
            self.session.close()
        else:
            self.session = Session()

    def all(self):
        """
        Récupère tous les enregitrements
        :return: list
        """
        self.newSession()
        return self.session.query(self.__modelClass__).all()

    def find(self, id):
        """
        Récupère un enregistrement
        :param id: id de l'enregistrement
        :return: object
        """
        self.newSession()
        return self.session.query(self.__modelClass__).get(id)

    def delete(self, id):
        """
        Supprime un enregistrement en base
        :param id: id de l'enregistrement
        :return: void
        """
        self.newSession()
        obj = self.session.query(self.__modelClass__).get(id)
        self.session.delete(obj)
        self.session.commit()
        self.session.flush()

    def save(self, obj):
        """
        Crée ou met à jour un enregistrement en base
        :param obj: l'objet à sauvegarder
        :return: void
        """
        self.newSession()
        self.session.add(obj)
        self.session.commit()
        self.session.flush()

    def __del__(self):
        """
        Ferme la session à la destruction de la classe
        :return:
        """
        self.session.close()


class CityService(GenericService):
    """
    Service pour le modèle City.
    """
    __modelClass__ = City

    def all_capitals(self):
        """
        Récupère toutes les villes qui sont des capitales
        :return: list
        """
        self.newSession()
        return self.session.query(City).filter(City.is_capital == 1).all()

    def all_non_capitals(self):
        """
        Récupère toutes les villes qui ne sont pas des capitales
        :return: list
        """
        self.newSession()
        return self.session.query(City).filter(City.is_capital == 0).all()

    def create(self, name, is_capital, country, capital_id):
        """
        Crée une ville à partir des champs d'un formulaire
        """
        city = City(name=name, is_capital=is_capital, country=country, capital_id=capital_id)
        self.save(city)


class TravelService(GenericService):
    """
    Service pour le modèle Travel.
    """
    __modelClass__ = Travel

    def all_capitals(self):
        """
        Récupère tous les voyages qui concernent une capitale
        :return: list
        """
        self.newSession()
        return self.session.query(Travel) \
            .join(City).filter(City.is_capital == 1) \
            .order_by(City.name).all()

    def all_by_budget(self):
        """
        Récupère tous les voyages triés par budget minimum
        (prix de l'hébergement + prix du transport)
        :return: list
        """
        return sorted(self.all(), key=lambda travel: travel.budget, reverse=False)

    def all_by_transport_duration(self):
        """
        Récupère tous les voyages triés par durée de transport minimum
        :return: list
        """
        return sorted(self.all(), key=lambda travel: travel.transport_duration, reverse=False)

    def create(self, city_id, start, end, review, accomodation_name, accomodation_type, accomodation_price,
               transport_type, transport_price, transport_duration):
        """
        Crée un voyage à partir des champs d'un formulaire
        """
        # Conversion des dates
        start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
        end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

        # Test de la validité des dates
        if start > end:
            raise ValueError()

        # Création du voyage
        travel = Travel(city_id=city_id, start=start_date, end=end_date, review=review)
        # Création de l'hébergement
        accomodation = Accomodation(name=accomodation_name, type=accomodation_type, price=accomodation_price)
        # Création d'un transport
        transport = Transport(type=transport_type, price=transport_price, duration=transport_duration)

        # Sauvegarde en base
        travel.accomodations.append(accomodation)
        travel.transports.append(transport)
        self.save(travel)


class TransportService(GenericService):
    """
    Service pour le modèle Transport.
    """
    __modelClass__ = Transport


class AccomodationService(GenericService):
    """
    Service pour le modèle Accomodation.
    """
    __modelClass__ = Accomodation
