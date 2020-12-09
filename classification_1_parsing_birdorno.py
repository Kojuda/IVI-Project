#!/usr/bin/env python
# coding=utf-8

"""
Ce script fait partie de la première classification. Le but est de classer les annonces selon
si elles mentionnent la présence d'oiseaux ou non. Selon des termes majoritairement anglais. Les
résultars sont stockés dans la table "classification_1_parse_bird_or_no"
"""

import time, json, re, datetime
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_bird_or_no
from ressources.regex_tools import word_to_regex

#Browse parsed title and description for each ad to estimate the number of (correctly classified) birds ads.
#Indeed, there are other things sold under pets/birds in adpost.com. For that, a list list_of_birds_test is created
#and the words of this list are compared to each word in each title and description. A regex function word_to_regex
#from ressources.regex_tools is applied to all of the words in list_of_birds_test to handle misspellings.
#The goal of this classification 1 is also to avoid false negatives as much as possible, accepting in consequence
#more false positives. In the end we have a broad idea of how many bird ads exist under pets/birds.

#Goal: Decide if an ad contains one/several bird/s
#Strategy: Look in "title" and "description" for words describing birds with regular expressions applied to these words
def create_regex_for_birds(list_of_birds_test):
    #At the beginning the list_of_birds is empty
    list_of_birds = []
    #For each element in list_of_birds_test
    for i in range(len(list_of_birds_test)):
        #apply the regexes with the function word_to_regex to all the words in list_of_birds_test
        a = word_to_regex(list_of_birds_test[i])
        print(a)
        #append the results to list_of_birds
        list_of_birds.append(a)
    return(list_of_birds)


if __name__ == '__main__':

    #Global variable which contains the expressions to match
    list_of_birds_test = ["bird", "brd", "amazon", "amazona", "parot", "prot", "african grey", "macaw", "mcw",
                          "macw", "mcaw", "macow", "cockato", "winged", "paraket", "lovebird", "canary", "cnry"]
    #list_of_birds is the list of each regular expression created with the words in list_of_birds_test
    list_of_birds = create_regex_for_birds(list_of_birds_test)
    print(list_of_birds)

    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    path_result = './results/classification/'

    #Parse database
    #Counter to trace vow many ads have status = 1 (classified as bird)
    c = 0
    for row in session.query(Parse_ads):

        #If ad (ad_id) not yet classified (0 or 1)
        if session.query(Parsing_bird_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None:

            #Step 1 : search in the title for each regular expression of list_of_birds
            for expression in list_of_birds:
                #The variable res is the string of the title
                res = re.search(str(expression), row.title)
                #If there is a match
                if res != None:
                    #And if there isn't already an entry
                    if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None:
                        #The entry is the ad_id and the status is 1
                        entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=1)
                        entry.insertParse_bird(session)
                        session.commit()
                        #Increment the counter by 1
                        c += 1
                        pass

            #Step 2 : search in the description for each regular expression of list_of_birds
            for expression in list_of_birds:
                #If a description exists for this ad
                if row.description != None:
                    try:
                        #The variable res is the string of the description
                        res = re.search(str(expression), row.description)
                    except:
                        #Otherwise raise and unknown error
                        print('unknown error')
                        print(row.ad_id)
                        res = None
                #If there is a match
                if res != None:
                    #And if there isn't already an entry
                    if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None:
                        #The entry is the ad_id and the status is 1
                        entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=1)
                        entry.insertParse_bird(session)
                        session.commit()
                        pass

            #Step 3 : if there is no match, status = 0
            if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == None:
                entry = Parsing_bird_or_no(ad_id=row.ad_id, status_bird=0)
                entry.insertParse_bird(session)
                session.commit()

        #If there are no matches in the title nor in the description, so if status bird = 0:
        else:
            if session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar() == 0:
                #print('change')
                status_change = True
                # step 1 search in title
                for expression in list_of_birds:
                    # For each defined regular expression
                    res = re.search(str(expression), row.title)  # search in title
                    if res != None:  # if there is a match, go on
                        if status_change:
                            #print('change stat')
                            Parsing_bird_or_no(ad_id=row.ad_id).update(session)
                            session.commit()
                            c += 1
                            status_change = True
                            pass
                    try:
                        res_des = re.search(str(expression), row.description)
                    except:
                        res_des = None
                    if res_des != None:
                        if status_change:
                            #print('change des')
                            Parsing_bird_or_no(ad_id=row.ad_id).update(session)
                            session.commit()
                            c += 1
                            status_change = True
                            pass

        #Write it to
        with open(f'./results/classification/documentation/bird_{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
