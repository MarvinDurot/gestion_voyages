"""
Facades de l'application
"""

from models import Travel, Transport, Accomodation, City, Session


class GenericFacade:
    """
    Facade générique permettant de manipuler
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
    def save(cls, obj):
        """
        Crée ou met à jour un enregistrement en base
        :param obj: l'objet à sauvegarder
        :return: void
        """
        cls.__session__.add(obj)
        cls.__session__.commit()
        cls.__session__.flush()


class CityFacade(GenericFacade):
    """
    Facade pour le modèle City.
    """
    __modelClass__ = City

    @classmethod
    def all_capitals(cls):
        """
        Récupère toutes les villes qui sont des capitales
        :return: list
        """
        return cls.__session__.query(City).filter(City.is_capital == 1).all()

    @classmethod
    def all_non_capitals(cls):
        """
        Récupère toutes les villes qui ne sont pas des capitales
        :return: list
        """
        return cls.__session__.query(City).filter(City.is_capital == 0).all()


class TravelFacade(GenericFacade):
    """
    Facade pour le modèle Travel.
    """
    __modelClass__ = Travel

    @classmethod
    def all_capitals(cls):
        """
        Récupère tous les voyages qui concernent une capitale
        :return: list
        """
        return cls.__session__.query(Travel, City) \
            .join(City).filter(City.is_capital == 1) \
            .order_by(City.name).all()

    @classmethod
    def all_by_budget(cls):
        """
        Récupère tous les voyages triés par budget minimum
        (prix de l'hébergement + prix du transport)
        :return: list
        """
        return sorted(cls.all(), key=lambda travel: travel.budget, reverse=True)

    @classmethod
    def all_by_transport_duration(cls):
        """
        Récupère tous les voyages triés par durée de transport minimum
        :return: list
        """
        return sorted(cls.all(), key=lambda travel: travel.transport_duration, reverse=True)


class TransportFacade(GenericFacade):
    """
    Facade pour le modèle Transport.
    """
    __modelClass__ = Transport


class AccomodationFacade(GenericFacade):
    """
    Facade pour le modèle Accomodation.
    """
    __modelClass__ = Accomodation
