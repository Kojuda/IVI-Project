#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import datetime
from sqlalchemy import create_engine #pip install sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


# class Url(Base):
#     __tablename__ = 'urls'
#     id = Column(Integer, primary_key=True)
#     url = Column(String, nullable=False)
#     status = Column(Integer, default=0)
#     date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
#     date_updated = Column(DateTime, onupdate=datetime.datetime.now())

# def insertURL(session, url):
#     url = Url(url=url)
#     session.add(url)
#     session.commit()

# def updateURL(session, url_object, newStatus=1):
#     url_object.status = newStatus
#     session.commit()

#~~~~~~~~~~~~~~~~~~~~~Create de base~~~~~~~~~~~~~~~~~~~~~
Base = declarative_base()



#~~~~~~~~~~~~~~~~~~~~~PROJET~~~~~~~~~~~~~~~~~~~~~

class Urls_ads(Base):
    __tablename__ = 'urls_ads'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    status = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    # country_id= Column(String, ForeignKey("coutries.id"))
    ad_number=Column(String, nullable=False)
    
    # country=relationship("Country", back_populates="urls_ads")
    def insertURL(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

class Country(Base) :
    __tablename__ = 'countries'
    id=Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    #urls_ads = country=relationship("Urls_ads", order_by=Urls_ads.id, back_populates="countries")

    def insertCountry(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()


#~~~~~~~~~~~~~~~~~~~~~Connect the database~~~~~~~~~~~~~~~~~~~~~

engine = create_engine('sqlite:///DATABASES/project.db') #, echo=True pour les log
Base.metadata.create_all(engine) #Create the database if it does not exist
Session = sessionmaker(bind=engine)
session = Session()










