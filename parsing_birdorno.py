#!/usr/bin/env python
# coding=utf-8
# author: J.Wyss
# creation: 13.11.2020
# But: parser le code client des publications de vente

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_bird_or_no
from spelling_error_mitigation import word_to_regex


#Goal 1: Decide if ad contains bird
#Strategy: Look in title for words describing birds with regular expressions
list_of_birds_test = ["bird","ara","amazon","amazona","parrot","african grey","macaw","cockatoo"] #Global variable which contains re to match
list_of_birds = []
for i in list_of_birds_test:
    a = word_to_regex(i)
    list_of_birds.append(a)
print(list_of_birds)

if __name__ == '__main__':
    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    #parse database
    c = 0 #counter to trace vow many ads have status 1 = classified as bird
    for row in session.query(Parse_ads):
        #step 1 search in title
        for expression in list_of_birds:
            #For each defined regular expression
            res = re.search(expression, row.title) #search in title
            if res != None: #if there is a match, go on
                if session.query(Parsing_bird_or_no.ad_id).filter_by(ad_id=row.ad_id, status_bird =1).scalar() == None: #if there isn't already an entry
                    entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=1)
                    entry.insertParse_bird(session)
                    session.commit()
                    c+=1
                    pass
        #step 2 search in description
        #description_list = []
        #if row.description != None:
        #    description_list = row.description.split(" ")
        for expression in list_of_birds:
            res = None
            if row.description != None:
                try:
                    res = re.search(expression, row.description)
                except:
                    print('unknown error')
                    print(row.ad_id)
            if res != None:
                if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() in [None, 0]:
                    print('description')
                    entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=1)
                    entry.insertParse_bird(session)
                    session.commit()
                    pass
        #last step if no match add status 0
        #if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()
        if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None:
            entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=0)
            entry.insertParse_bird(session)
            session.commit()

