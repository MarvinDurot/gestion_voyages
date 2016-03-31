from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3', echo=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    isCapital = Column(Boolean, nullable=False, default=False)
    country = Column(String, nullable=False)
    capitalId = Column(ForeignKey('City.id'), nullable=True)

    def __init__(self, id, name, isCapital, country, capitalId):
        self.id = id
        self.name = name
        self.isCapital = isCapital
        self.country = country
        self.capitalId = capitalId

class Travel(Base):
    __tablename__ = 'travels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    review = Column(String, nullable=True)
    cityId = Column(Integer, ForeignKey('City.id'), nullable=False)
    transports = relationship('Transport', backref=backref('transports', uselist=True, cascade='delete,all'))
    accomodations = relationship('Accomodation', backref=backref('accomodations', uselist=True, cascade='delete,all'))

    def __init__(self, id, date, duration, review, cityId, transports, accomodations):
        self.id = id
        self.date = date
        self.duration = duration
        self.review = review
        self.cityId = cityId
        self.transports = transports
        self.accomodations = accomodations

class Transport(Base):
    __tablename__ = 'transports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('Voiture', 'Train', 'Avion', 'Bateau'), nullable=False)
    price = Column(Numeric(2, 4), nullable=False)
    duration = Column(Integer, nullable=False)
    travelId = Column(ForeignKey('Travel.id'), nullable=False)

    def __init__(self, id, type, price, duration, travelId):
        self.id = id
        self.type = type
        self.price = price
        self.duration = duration
        self.travelId = travelId

class Accomodation(Base):
    __tablename__ = 'accomodations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('Hôtel', 'Gîte', 'Location', 'Camping'), nullable=False)
    price = Column(Numeric(2, 4), nullable=False)
    travelId = Column(ForeignKey('Travel.id'), nullable=False)

    def __init__(self, id, name, type, price, travelId):
        self.id = id
        self.name = name
        self.type = type
        self.price = price
        self.travelId = travelId

Base.metadata.create_all(engine)