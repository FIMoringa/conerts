from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (create_engine, PrimaryKeyConstraint,
                        Column, String, Integer, ForeignKey)
import os
import sys

sys.path.append(os.getcwd)


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

    def concerts(self):
        return self.concerts

    def venues(self):
        return self.venues


# Concert hometown_show()
# returns true if the concert is in the band's hometown, false if it is not


    def hometown_show(self):
        for concert in self.concerts:
            if concert.venue.city == self.hometown:
                return True
        return False

    def upcoming_shows(self):
        upcoming_shows = []
        for concert in self.concerts:
            if concert.date > datetime.now():
                upcoming_shows.append(concert)
        return upcoming_shows

#    Concert introduction()
# returns a string with the band's introduction for this concert
# an introduction is in the form:
# "Hello {insert venue city}!!!!! We are {insert band name} and we're from
# {insert band hometown}"

    def introduction(self):
        return f'Hello {self.concerts[0].venue.city}!!!!! We are {self.name} and we are from {self.hometown}'

    # Band play_in_venue(venue, date)
# takes a venue (Venue instance) and date (as a string) as arguments
# creates a new concert for the band in that venue on that date

    def play_in_venue(self, venue, date):
        concert = Concert(date=date, band=self, venue=venue)
        return concert

# Band all_introductions()
# returns an array of strings representing all the introductions for this band
# each introduction is in the form:

    def all_introductions(self):
        introductions = []
        for concert in self.concerts:
            introductions.append(
                f'Hello {concert.venue.city}!!!!! We are {self.name} and we are from {self.hometown}')
        return introductions
class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    city = Column(String())
    band_id = Column(Integer, ForeignKey('bands.id'))

    band = relationship('Band', backref=backref(
        'venues', uselist=True, cascade='delete,all'))

    def __repr__(self):
        return f'Venue: {self.name}'

    def concerts(self):
        return self.concerts

    def bands(self):
        return self.bands


class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    date = Column(String())
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    band = relationship('Band', backref=backref(
        'concerts', uselist=True, cascade='delete,all'))
    venue = relationship('Venue', backref=backref(
        'concerts', uselist=True, cascade='delete,all'))

    def band_name(self):
        return self.band.name

    def venue_name(self):
        return self.venue.title

    def __repr__(self):
        return f'Concert: {self.date}'
