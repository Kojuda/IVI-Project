#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import datetime
from sqlalchemy import create_engine #pip install sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    status = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now())

def insertURL(session, url):
    url = Url(url=url)
    session.add(url)
    session.commit()

def updateURL(session, url_object, newStatus=1):
    url_object.status = newStatus
    session.commit()

engine = create_engine('sqlite:///urlToCrawl.db') #, echo=True pour les log
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
