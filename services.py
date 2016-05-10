"""
Services de l'application
"""

from models import Travel, Transport, Accomodation, City, Session


class GenericService:
    """
    Service générique permettant de manipuler
    les modèles en base plus simplement.
    """
    __modelClass__ = None
    __session__ = Session()

    @classmethod
    def all(cls):
        """
        Récupère tous les enregitrements
        :return: list
        """
        return cls.__session__.query(cls.__modelClass__).all()

    @classmethod
    def find(cls, id):
        """
        Récupère un enregistrement
        :param id: id de l'enregistrement
        :return: object
        """
        return cls.__session__.query(cls.__modelClass__).get(id)

    @classmethod
    def delete(cls, id):
        """
        Supprime un enregistrement en base
        :param id: id de l'enregistrement
        :return: void
        """
        obj = cls.find(id)
        cls.__session__.delete(obj)
        cls.__session__.commit()
        cls.__session__.flush()

    @classmethod
    def create(cls, obj):
        """
        Crée un nouvel enregistrement en base
        :param obj: l'objet correspondant à l'enregistrement à supprimer
        :return: void
        """
        cls.__session__.add(obj)
        cls.__session__.commit()
        cls.__session__.flush()


class CityService(GenericService):
    """
    Service pour le modèle City.
    """
    __modelClass__ = City


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
        return self.__session__.query(Travel, City) \
            .join(City).filter(City.isCapital == 1) \
            .order_by(City.name).all()

    def all_by_budget(self):
        """
        Récupère tous les voyages triés par budget minimum
        (prix de l'hébergement + prix du transport)
        :return: list
        """
        return self.__session__.query(Travel).order_by(Travel.budget).all()

    def all_by_transport_duration(self):
        """
        Récupère tous les voyages triés par durée de transport minimum
        :return: list
        """
        return self.__session__.query(Travel).order_by(Travel.transport_duration).all()


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
