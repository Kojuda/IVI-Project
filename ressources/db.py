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
from sqlalchemy import MetaData, Table, Column, Integer, String


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
    title = Column(String)
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

    def deleteEntry(self, session) :
        session.delete(self)
        session.commit()

class Parsing_bird_or_no(Base):
    __tablename__ = 'parse_bird_or_no'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, ForeignKey("parse_ads.ad_id"))
    status_bird = Column(Integer, default=0)#0: not classified 1: classified

    parse_ads = relationship("Parse_ads", backref="parse_bird_or_no")
    def insertParse_bird(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class MentionedCage(Base):
    __tablename__ = 'cage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, ForeignKey("parse_ads.ad_id"))
    status_cage = Column(Integer, default=0)#0: not classified 1: classified
    status_alerte = Column(Integer, default=0)#0:alright 1: contains words with waarant recheck of classification

    parse_ads = relationship("Parse_ads", backref="cage")
    def insertCage(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class Parsing_Psittaciformes_or_no(Base):
    __tablename__ = 'psittaciformes_or_no'
    #H: une même annonce ne match pas plus que 10 noms d'oiseaux différents
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, ForeignKey("parse_ads.ad_id"))
    match_cites_parrot = Column(Integer, default=0)#0: not classified 1: classified
    match_common_parrot = Column(Integer, default=0)#0: not classified 1: classified
    mapping_match_1 = Column(Integer, ForeignKey("mapping_cites.id")) #première fois que ça match
    #mapping_match_2 = Column(Integer, ForeignKey("mapping_cites.id")) #deuxième fois que ça match, etc.
    #mapping_match_3 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_4 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_5 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_6 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_7 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_8 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_9 = Column(Integer, ForeignKey("mapping_cites.id"))
    #mapping_match_10 = Column(Integer, ForeignKey("mapping_cites.id"))
    parse_ads = relationship("Parse_ads", backref="psittaciformes_or_no")
    mapping_cites = relationship("Mapping", backref="psittaciformes_or_no")
    def insertPsittaciformes(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class Mapping(Base):
    __tablename__ = 'mapping_cites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    scientific_name_cites = Column(String)
    common_name = Column(String)
    region = Column(String)
    danger_status_UCIN = Column(String)
    slang = Column(String)
    annex_number_CITES = Column(Integer)
    order = Column(String)
    family = Column(String)
    #pas de relation avec une autre table
    #parse_ads = relationship("Parse_ads", backref="psittaciformes_or_no")

    def insert(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()
#~~~~~~~~~~~~~~~~~~~~~Connect the database~~~~~~~~~~~~~~~~~~~~~

engine = create_engine('sqlite:////Users/pintorodriguesanaluisa/Desktop/Docs/ESC/4.3/IVI/Projet/IVI-Project/DATABASES/project.db') #, echo=True pour les log
    #j'ai changé ../ pour que ça crée la DB sinon ça marchait pas car pas dans le même dossier [a faire entre Luisa&autres]
    #engine = create_engine('sqlite:///C:\\Users\\Jasmin\\Documents\\GitHub\\IVI-Project\\DATABASES\\project.db') #, echo=True pour les log
    #pour luisa la path est: 'sqlite:////Users/pintorodriguesanaluisa/Desktop/Docs/ESC/4.3/IVI/Projet/IVI-Project/DATABASES/project.db'
Base.metadata.create_all(engine) #Create the database if it does not exist
Session = sessionmaker(bind=engine)
session = Session()

#~~~~~~~~~~~~~~~Create a table~~~~~~~~~~~~~~~~
#meta = MetaData()
#parse_bird_or_no = Table('parse_bird_or_no', meta,
#                         Column('id', Integer, primary_key = True, nullable=False, autoincrement=True),
#                         Column('ad_id', String(32)),
#                         Column('status_bird', Integer, default=0))
#meta.create_all(engine)
