"""
Modèles de l'application
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3', echo=False)
Session = sessionmaker(bind=engine, autoflush=False)


class City(Base):
    """
    Représentation en base d'une ville.
    """
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_capital = Column(Boolean, nullable=False, default=False)
    country = Column(String, nullable=False)
    capital_id = Column(Integer, ForeignKey('cities.id'), nullable=True)
    capital = relationship('City', remote_side=[id], lazy='joined')

    @hybrid_property
    def nearest_capital(self):
        if self.is_capital:
            return self.name
        else:
            return self.capital.name

    def __repr__(self):
        return "City (name=%s, nearest_capital=%s, country=%s)" % (self.name, self.nearest_capital, self.country)

    def input(self):
        self.name = str(input("Nom?"))
        self.is_capital = bool(input("Est une capitale? (0,1) "))
        self.country = str(input("Pays? "))
        self.capital_id = int(input("Capitale la plus proche? "))


class Travel(Base):
    """
    Représentation en base d'un voyage.
    """
    __tablename__ = 'travels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    review = Column(String, nullable=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    transports = relationship('Transport', backref=backref('transports', uselist=True, cascade='delete,all'))
    accomodations = relationship('Accomodation', backref=backref('accomodations', uselist=True, cascade='delete,all'))
    city = relationship('City', lazy='joined')

    @hybrid_property
    def budget(self):
        transport_prices = [transport.price for transport in self.transports]
        accomodations_prices = [accomodation.price for accomodation in self.accomodations]
        return min(transport_prices) + min(accomodations_prices)

    @hybrid_property
    def transport_duration(self):
        transport_durations = [transport.duration for transport in self.transports]
        return min(transport_durations)

    def input(self):
        self.start = datetime.datetime.strptime(input("Date de départ? "), "%d/%m/%Y")
        self.end = datetime.datetime.strptime(input("Date de retour? "), "%d/%m/%Y")
        self.review = str(input("Avis sur la ville ? "))
        self.city_id = int(input("Ville? "))

    def __repr__(self):
        return "Travel (city=%s, start=%s, end=%s)" % (
            self.city.name, self.start.strftime("%d-%m-%Y"), self.end.strftime("%d-%m-%Y"))


class Transport(Base):
    """
    Représentation en base d'un transport.
    """
    __tablename__ = 'transports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('Voiture', 'Train', 'Avion', 'Bateau', 'Bus'), nullable=False)
    price = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    travel_id = Column(Integer, ForeignKey('travels.id'), nullable=False)
    travel = relationship('Travel', backref=backref('transports', cascade="all,delete"))

    def input(self):
        self.type = str(input("Type? "))
        self.price = int(input("Prix? "))
        self.duration = int(input("Durée? "))

    def __repr__(self):
        return "Transport (type=%s, price=%d, duration=%d)" % (
            self.type, self.price, self.duration)


class Accomodation(Base):
    """
    Représentation en base d'un hébergement.
    """
    __tablename__ = 'accomodations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('Hôtel', 'Gîte', 'Appartement', 'Camping'), nullable=False)
    price = Column(Integer, nullable=False)
    travel_id = Column(Integer, ForeignKey('travels.id'), nullable=False)
    travel = relationship('Travel', backref=backref('accomodations', cascade="all,delete"))

    def input(self):
        self.name = str(input("Nom? "))
        self.type = str(input("Type? "))
        self.price = int(input("Prix? "))

    def __repr__(self):
        return "Accomodation (name=%s, type=%s, price=%d)" % (self.name, self.type, self.price)


if __name__ == '__main__':
    # Crée la base de données à partir du méta modèle
    Base.metadata.create_all(engine)
