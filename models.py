"""
Modèles de l'application
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3', echo=False)
Session = sessionmaker(bind=engine)


class City(Base):
    """
    Représentation en base d'une ville.
    """
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    isCapital = Column(Boolean, nullable=False, default=False)
    country = Column(String, nullable=False)
    capitalId = Column(Integer, ForeignKey('cities.id'), nullable=True)

    def __repr__(self):
        return "City (name=%s, isCapital=%r, country=%s)" % (self.name, self.isCapital, self.country)

    def input(self):
        self.name = str(input("Nom?"))
        self.isCapital = bool(input("Est une capitale? (0,1) "))
        self.country = str(input("Pays? "))
        self.capitalId = int(input("Capitale la plus proche? "))


class Travel(Base):
    """
    Représentation en base d'un voyage.
    """
    __tablename__ = 'travels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    review = Column(String, nullable=True)
    cityId = Column(Integer, ForeignKey('cities.id'), nullable=False)
    transports = relationship('Transport', backref=backref('transports', uselist=True, cascade='delete,all'))
    accomodations = relationship('Accomodation', backref=backref('accomodations', uselist=True, cascade='delete,all'))

    def input(self):
        self.start = datetime.datetime.strptime(input("Date de départ? "), "%d/%m/%Y")
        self.end = datetime.datetime.strptime(input("Date de retour? "), "%d/%m/%Y")
        self.review = str(input("Avis sur la ville ? "))
        self.cityId = int(input("Ville? "))

    def __repr__(self):
        return "Travel (start=%s, end=%s, review=%s)" % (
            self.start.strftime("%d-%m-%Y"), self.end.strftime("%d-%m-%Y"), self.review)


class Transport(Base):
    """
    Représentation en base d'un transport.
    """
    __tablename__ = 'transports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('Voiture', 'Train', 'Avion', 'Bateau'), nullable=False)
    price = Column(Numeric(2, 4), nullable=False)
    duration = Column(Integer, nullable=False)
    travelId = Column(Integer, ForeignKey('travels.id'), nullable=False)

    def input(self):
        self.type = str(input("Type? "))
        self.price = float(input("Prix? "))
        self.duration = int(input("Durée? "))

    def __repr__(self):
        return "Transport (type=%s, price=%d, duration=%d)" % (self.type, self.price, self.duration)


class Accomodation(Base):
    """
    Représentation en base d'un hébergement.
    """
    __tablename__ = 'accomodations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('Hôtel', 'Gîte', 'Location', 'Camping'), nullable=False)
    price = Column(Numeric(2, 4), nullable=False)
    travelId = Column(Integer, ForeignKey('travels.id'), nullable=False)

    def input(self):
        self.name = str(input("Nom? "))
        self.type = str(input("Type? "))
        self.price = float(input("Prix? "))

    def __repr__(self):
        return "Accomodation (name=%s, type=%s, price=%d)" % (self.name, self.type, self.price)


Base.metadata.create_all(engine)
