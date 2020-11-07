#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# adapte par: Danny Kohler, Luisa Rodrigues, Jasmin Wyss
# creation: 06.10.2020

import datetime
from sqlalchemy import create_engine #pip install sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


#~~~~~~~~~~~~~~~~~~~~~Create de base~~~~~~~~~~~~~~~~~~~~~
Base = declarative_base()



#~~~~~~~~~~~~~~~~~~~~~PROJET~~~~~~~~~~~~~~~~~~~~~

class Country(Base) :
    __tablename__ = 'countries'
    id=Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    def insertCountry(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()


class Urls_ads(Base):
    __tablename__ = 'urls_ads'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    ad_id = Column(String, unique=True)
    ad_number=Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    status = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    country_id= Column(Integer, ForeignKey("countries.name"))

    #code = relationship("Ads_Codes_tmp", back_populates="urls_ads_tmp", uselist=False)
    country=relationship("Country", backref="urls_ads")
    def insertURL(self, session):
        session.add(self)
        session.commit()

    def urls_ads_update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

class Ads_Codes(Base):
    __tablename__='ads_codes'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    ad_id = Column(String, ForeignKey("urls_ads.ad_id"), unique=True)
    ad_number = Column(Integer, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    client_code = Column(String, nullable=False)
    status = Column(Integer, default=0)#Parsing yes=1,no=0
    status_image_taken = Column(Integer, default=0)#Image extrait: yes=1, no=0
    status_vendeur_taken = Column(Integer, default=0)#Vendeur extrait: yes=1, no=0


    urls_ads_tmp = relationship("Urls_ads", backref="ads_codes")
    def insertCode(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()




class Parse_ads(Base):
    __tablename__='parse_ads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    ad_id = Column(String, ForeignKey("ads_codes.ad_id"), unique=True)
    ad_number = Column(Integer, nullable=False)
    category = Column(String)
    description = Column(String)
    breed = Column(String)
    age = Column(Integer)
    sex = Column(String)
    primary_color = Column(String)
    secondary_color = Column(String)
    advertiser = Column(String)
    price = Column(Integer)
    payment_forms = Column(String)
    estimated_shipping = Column(String)
    pseudo = Column(String)
    contact_information = Column(String)
    name = Column(String)
    company=  Column(String)
    zip = Column(Integer)
    city = Column(String)
    state = Column(String)
    county = Column(String)
    country = Column(String)
    region = Column(String)
    province = Column(String)
    email = Column(String)
    phone = Column(Integer)
    redirect_website= Column(String)
    status_vendeur_taken = Column(Integer, default=0)

    ads_codes = relationship("Ads_Codes", backref="parse_ads")
    def insertParse_ads(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

#~~~~~~~~~~~~~~~~~~~~~Connect the database~~~~~~~~~~~~~~~~~~~~~

engine = create_engine('sqlite:///DATABASES/project.db') #, echo=True pour les log
    #j'ai changé ../ pour que ça crée la DB sinon ça marchait pas car pas dans le même dossier [a faire entre Luisa&autres]
Base.metadata.create_all(engine) #Create the database if it does not exist
Session = sessionmaker(bind=engine)
session = Session()

