"""
Services de l'application
"""

from models import Travel, Transport, Accomodation, City


class GenericService:
    """
    Service générique permettant de manipuler
    les modèles en base plus simplement.
    """
    __modelClass__ = None

    def __init__(self, session):
        """
        Constructeur
        :param session: session SQLAlchemy
        :return: void
        """
        self.session = session

    def all(self):
        """
        Récupère tous les enregitrements
        :return: list
        """
        return self.session.query(self.__modelClass__).all()

    def find(self, id):
        """
        Récupère un enregistrement
        :param id: id de l'enregistrement
        :return: object
        """
        return self.session.query(self.__modelClass__).get(id)

    def delete(self, id):
        """
        Supprime un enregistrement en base
        :param id: id de l'enregistrement
        :return: void
        """
        obj = self.find(id)
        self.session.delete(obj)
        self.session.commit()
        self.session.flush()

    def save(self, obj):
        """
        Crée ou met à jour un enregistrement en base
        :param obj: l'objet à sauvegarder
        :return: void
        """
        self.session.add(obj)
        self.session.commit()
        self.session.flush()


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
        return self.session.query(City).filter(City.is_capital == 1).all()

    def all_non_capitals(self):
        """
        Récupère toutes les villes qui ne sont pas des capitales
        :return: list
        """
        return self.session.query(City).filter(City.is_capital == 0).all()


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
