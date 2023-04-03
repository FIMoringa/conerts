import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_engine('sqlite:///db/concerts.db', echo=True)

# class Concert(Base):
#     pass

# Band has many Concerts, a Venue has many Concerts, and a Concert belongs to a Band and to a Venue.
class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    hometown = Column(String())


    def __repr__(self):
        return f'Band: {self.name}'


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    city = Column(String())

    def __repr__(self):
        return f'Venue: {self.name}'
    
    def concerts(self):
        return self.concerts

class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    date = Column(String())
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    band = relationship('Band', backref=backref('concerts', uselist=True, cascade='delete,all'))
    venue = relationship('Venue', backref=backref('concerts', uselist=True, cascade='delete,all'))

    def band_name(self):
        return self.band.name

    def venue_name(self):
        return self.venue.title

    def __repr__(self):
        return f'Concert: {self.date}'