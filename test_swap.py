#!/usr/bin/env python
# coding=utf-8
# But: parser le code client des publications de vente

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_bird_or_no
from spelling_error_mitigation import word_to_regex


#Goal 1: Decide if ad contains bird
#Strategy: Look in title for words describing birds with regular expressions
list_of_birds_test = ["bird","brd","amazon","amazona","parot", "prot", "african grey","macaw","mcw","macw","mcaw","macow","cockato","winged","paraket"] #Global variable which contains re to match
list_of_birds = []
for i in list_of_birds_test:
    a = word_to_regex(i)
    list_of_birds.append(a)

if __name__ == '__main__':
    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    #parse database
    c = 0 #counter to trace vow many ads have status 1 = classified as bird
    for row in session.query(Parse_ads):
        if session.query(Parsing_bird_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None:
        #step 1 search in title
            for expression in list_of_birds:
                #For each defined regular expression
                res = re.search(expression, row.title) #search in title
                if res != None: #if there is a match, go on
                    if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None: #if there isn't already an entry
                        entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=1)
                        entry.insertParse_bird(session)
                        session.commit()
                        c+=1
                        pass
        #step 2 search in description
            for expression in list_of_birds:
                if row.description != None:
                    try:
                        res = re.search(expression, row.description)
                    except:
                        print('unknown error')
                        print(row.ad_id)
                        res = None
                if res != None:
                    if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None:
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

        else:
            #print(session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar(), type(session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()))
            if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()==0:
                print('change')
                status_change = False
                # step 1 search in title
                for expression in list_of_birds:
                    # For each defined regular expression
                    res = re.search(expression, row.title)  # search in title
                    if res != None:  # if there is a match, go on
                        if status_change:
                            Parsing_bird_or_no(ad_id=row.ad_id).update(session)
                            session.commit()
                            c += 1
                            status_change = True
                            pass
                    res_des = re.search(expression, row.description)
                    if res_des != None:
                        if status_change:
                            Parsing_bird_or_no(ad_id=row.ad_id).update(session)
                            session.commit()
                            c += 1
                            status_change = True
                            pass
