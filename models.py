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


class User(Base):
    """
    Représentation en base d'un utilisateur.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return "User (login=%s, password=%s)" % (self.login, self.password)


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

    def __init__(self, name, isCapital, country, capitalId):
        self.name = name
        self.isCapital = isCapital
        self.country = country
        self.capitalId = capitalId

    def __repr__(self):
        return "City (name=%s, isCapital=%r, country=%s)" % (self.name, self.isCapital, self.country)


class Travel(Base):
    """
    Représentation en base d'un voyage.
    """
    __tablename__ = 'travels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    review = Column(String, nullable=True)
    cityId = Column(Integer, ForeignKey('cities.id'), nullable=False)
    transports = relationship('Transport', backref=backref('transports', uselist=True, cascade='delete,all'))
    accomodations = relationship('Accomodation', backref=backref('accomodations', uselist=True, cascade='delete,all'))

    def __init__(self, date, duration, review, cityId, transports, accomodations):
        self.date = datetime.datetime.strptime(date, "%d/%m/%Y")
        self.duration = duration
        self.review = review
        self.cityId = cityId
        self.transports = transports
        self.accomodations = accomodations

    def __repr__(self):
        return "Travel (date=%s, duration=%d, review=%s)" % (self.date.strftime("%d-%m-%Y"), self.duration, self.review)


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

    def __init__(self, type, price, duration):
        self.type = type
        self.price = price
        self.duration = duration

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

    def __init__(self, name, type, price):
        self.name = name
        self.type = type
        self.price = price

    def __repr__(self):
        return "Accomodation (name=%s, type=%s, price=%d)" % (self.name, self.type, self.price)


Base.metadata.create_all(engine)
