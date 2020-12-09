#!/usr/bin/env python
# creation: 06.10.2020

"""Ressource qui permet d'établir un interpréteur des tables de la base de données SQL
avec sqlalchemy. Les colonnes et leur contraintes, le nom des tables et les fonctions pour
interagir avec sont notamment définis dans la ressource."""

import datetime
from sqlalchemy import create_engine #pip install sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import JSON


#~~~~~~~~~~~~~~~~~~~~~Create de base~~~~~~~~~~~~~~~~~~~~~
Base = declarative_base()

#~~~~~~~~~~~~~~~~~~~~~PROJET~~~~~~~~~~~~~~~~~~~~~

class Country(Base) :
    """Table containing the country related to the folders of Adpost.com
    et the urls of these."""

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
    """Table containing the extracted urls of the ads with their unique
    identifier. Table linked to the table Country by the country value."""

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
    """Table containing the name of the extracted client code file and a status
    for the parsing. Table linked to the table Urls_Ads by the ad_id"""

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
<<<<<<< HEAD
     """Table containing the raw parsed field of the ads from the client code. Table linked to the table Ads_Code by the ad_id"""
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
    """Table containing the status about the presence of birds
    in the ads according to the classification 1."""

    __tablename__ = 'classification_1_parse_bird_or_no'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, unique=True) #ForeignKey("parse_ads.ad_id")
    status_bird = Column(Integer, default=0)#0: not classified 1: classified

    #parse_ads = relationship("Parse_ads", backref="parse_bird_or_no")
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
    """Table containing the status about the presence of cages
    in the ads according to the classification 1."""

    __tablename__ = 'classification_1_cage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, unique=True) #ForeignKey("parse_ads.ad_id")
    status_cage = Column(Integer, default=0)#0: not classified 1: classified
    status_alerte = Column(Integer, default=0)#0:alright 1: contains words with waarant recheck of classification

    #parse_ads = relationship("Parse_ads", backref="cage")
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
    """Table containing the status about the presence of parrots
    in the ads according to the classification 1. Show the list of
    matched words according to a lexic about parrots and the CITES
    specices."""

    __tablename__ = 'classification_1_psittaciformes_or_no'
    #H: une même annonce ne match pas plus que 10 noms d'oiseaux différents
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, unique=True) #ForeignKey("parse_ads.ad_id")
    match_cites_parrot = Column(Integer, default=0)#0: not classified 1: classified
    match_common_parrot = Column(Integer, default=0)#0: not classified 1: classified
    mapping_match = Column(String) #en gros les differents matches_regex separée par ;

    #parse_ads = relationship("Parse_ads", backref="psittaciformes_or_no")
    #mapping_cites = relationship("Mapping", backref="psittaciformes_or_no")
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
    """The table provides the list of parrot species from CITES according
    to their appendice. Thus a list of common names has been added manually
    per species to perform the classification."""

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

    def insert(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class Regex(Base):
    """Table containing the regexes per word used to perform
    the classification 1"""

    __tablename__ = 'classification_1_regex'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reg = Column(String)
    word = Column(String)


    def insertregex(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()


class Match_Regex_IdMap(Base):
    """Table containing the link between the matched regexes of the
    classification 1 and the CITES species from the mapping."""

    __tablename__ = 'classification_1_reg_map_match'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_re = Column(Integer) #ForeignKey("classification_1_regex.id")
    id_map = Column(Integer) #ForeignKey("mapping_cites.id")
    #pas de relation avec une autre table
    #mapping_cites = relationship("Mapping", backref="reg_map_match")
    #regex = relationship("Regex", backref="reg_map_match")

    def insertMatch(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class Classification_2_Ads(Base):
    """Table containing the list of matched CITES species per ad according to
    the classification 2 including mentions of eggs, parrots, cages, birds and
    CITES registration papers. Thus the matched regexes are included in JSON format."""

    __tablename__ = 'classification_2_matching_ads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String,  unique=True)#ForeignKey("parse_ads.ad_id")
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    ids_matching = Column(String)
    parrot=Column(Integer)
    regex = Column(JSON)
    nb_species_matches= Column(Integer)
    cage= Column(Integer)
    egg=Column(Integer)
    cites_paper=Column(Integer)
    cites_appendice=Column(Integer)
    status=Column(Integer, default=0)

    def insert(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()

class Classification_3_Ads(Base):
    """Table containing the list of matched CITES species per ad according to
    the classification 3 including mentions of eggs, parrots, cages, birds and
    CITES registration papers. Thus the matched regexes are included in JSON format."""

    __tablename__ = 'classification_3_matching_ads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String,  unique=True)#ForeignKey("parse_ads.ad_id")
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())
    ids_matching = Column(String)
    parrot=Column(Integer)
    regex = Column(JSON)
    nb_species_matches= Column(Integer)
    cage= Column(Integer)
    egg=Column(Integer)
    cites_paper=Column(Integer)
    cites_appendice=Column(Integer)
    status=Column(Integer, default=0)

    def insert(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session):
        session.delete(self)
        session.commit()


class Vendor_analyse(Base):
    """Table containing the parsed list of vendors with their information
    form the parse_ads table."""

    __tablename__='vendor_analyse'
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    email_description = Column(String)
    phone = Column(Integer)
    phone_description = Column(Integer)
    redirect_website= Column(String)
    website_deviate = Column(String)
    status_vendeur_taken = Column(Integer, default=0)
    status_bird = Column(Integer)

    def insertVendor_analyse(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status_bird = newStatus
        session.commit()

    def deleteEntry(self, session) :
        session.delete(self)
        session.commit()


class Ads_clean(Base):
    """Table containing the parsed fields of the parse_ads table to be
    easily used by analysis tools."""

    __tablename__='ads_clean'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(String, unique=True)
    ad_number = Column(Integer, nullable=False)
    id_vendor=Column(Integer)
    title = Column(String)
    description = Column(String)
    breed = Column(String)
    age = Column(Integer)
    sex = Column(String)
    primary_color = Column(String)
    secondary_color = Column(String)
    price = Column(Integer)
    currency = Column(String)
    price_in_dollar = Column(String)
    payment_forms = Column(String)

    def insertAds_clean(self, session):
        session.add(self)
        session.commit()

    def update(self, session, newStatus=1):
        self.status = newStatus
        session.commit()

    def deleteEntry(self, session) :
        session.delete(self)
        session.commit()



#~~~~~~~~~~~~~~~~~~~~~Connect the database~~~~~~~~~~~~~~~~~~~~~


engine = create_engine('sqlite:///C://Users//Jasmin//switchdrive//DATABASES//project.db')
#change for others...
#relative path: 'sqlite:///results/DATABASES/project.db'
# Jasmin's machine: 'sqlite://C://Users//Jasmin//switchdrive//DATABASES//project.db'
Base.metadata.create_all(engine) #Create the database if it does not exist
Session = sessionmaker(bind=engine)
session = Session()