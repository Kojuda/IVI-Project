#!/usr/bin/env python
# coding=utf-8
# author: J.Wyss
# creation: 13.11.2020
# But: parser le code client des publications de vente

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_bird_or_no

#Goal 1: Decide if ad contains bird
#Strategy: Look in title for words describing birds with regular expressions
list_of_birds_test = ["bird","Bird","Ara","ara","Amazon","amazon","amazona","Amazona","Parrot","parrot","African Grey","african grey","macaw","Macaw"] #Global variable which contains re to match
if __name__ == '__main__':
    path_result = './results/parse/'
    #Documentation

    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    #parse database
    c = 0
    for row in session.query(Parse_ads):
        try:
            exists = session.query(Parsing_bird_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar()
        except:
            exists = None
        if exists == None:
            for expression in list_of_birds_test: #For each defined regular expression
                res = re.search(expression, row.title) #search in title
                if res != None: #if there is a match, go on
                    #entry = Parsing_bird_or_no(ad_id=row.ad_id)
                    #entry.insertParse_bird(session)
                    #Parsing_bird_or_no.update()
                    #session.commit()
                    c+=1
            description_list = []
            if row.description != None:
                description_list = row.description.split(" ")
            for expression in list_of_birds_test:
                if expression in description_list:
                    c+=1
        else:
            pass
    print(c)
