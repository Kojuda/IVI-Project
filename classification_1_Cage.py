#!/usr/bin/env python
# coding=utf-8

"""
Ce script fait partie de la première classification. Il cherche à établir la présence
de cage dans les annonces qui contriburait au taux de faux-positifs.
Il était constate que il y a trop de faux positifs si les mots 'cage' sont charche dans la description,
donc uniquement le titre est cherchée.
Les résultats sont stockés dans la table "classification_1_cage"
cette script était pas encore finalisée au moment ou il était decidée de favoriser la classification 2 & 3$
Mais ce script pourrait être adaptée pour aussi chercher les oefs oz des autres informations compléementaires à une annonce
"""

import re, datetime
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, MentionedCage
from spelling_error_mitigation import word_to_regex

cagenames = [" cage "] #Global variable which contains re to match
alerte = ['with'] #si plus qu'un mot code doit être changé

def return_list_of_cage():
    """returns list with regex of names describing cages"""
    list_of_cage = []
    for i in cagenames:
        a = word_to_regex(i)
        list_of_cage.append(a)
    return list_of_cage

def return_liste_alerte():
    """returns list with regex of names describing words considered to indicate cage and bird are conjointly sold"""
    list_alerte = []
    for i in alerte:
        a = word_to_regex(i)
        list_alerte.append(a)
    return list_alerte

if __name__ == '__main__':
    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    #parse database
    list_of_cage = return_list_of_cage()
    list_alerte = return_liste_alerte()
    for row in session.query(Parse_ads):
        if session.query(MentionedCage.ad_id).filter_by(ad_id=row.ad_id).scalar() == None: #if there is no entry already for the given ad_id
            for expression in list_of_cage: #For each defined regular expression
                res = re.search(expression, row.title) #search in title
                if res != None: #if there is a match, go on
                    if session.query(MentionedCage.status_cage).filter_by(ad_id=row.ad_id).scalar() == None: #if there isn't already an entry
                        for al in list_alerte:
                            #pour l'instant ca marche que pour 1 mot d'alerte, changer si besoin
                            try:
                                alert = re.search(al, row.title)
                            except:
                                alerte = None
                        if alerte == None:
                            entry = MentionedCage(ad_id=row.ad_id, status_cage=1)
                        else:
                            entry = MentionedCage(ad_id=row.ad_id, status_cage=1, status_alerte=1)
                        entry.insertCage(session)
                        session.commit()
                        pass
            if session.query(MentionedCage.status_cage).filter_by(ad_id=row.ad_id).scalar() == None: #if there is no entry yet made there musn't be a cage detected
                entry = MentionedCage(ad_id=row.ad_id, status_cage=0) #create non-entry
                entry.insertCage(session)
                session.commit()

        else:
            if session.query(MentionedCage.status_cage).filter_by(ad_id=row.ad_id).scalar()==0: #if there is an entry, but no cage has been detected we recheck
                status_change = False #if the status hasn't changed yet
                for expression in list_of_cage:
                    # For each defined regular expression
                    res = re.search(expression, row.title)  # search in title
                    if res != None:  # if there is a match, go on
                        if not status_change: #change status, update entry
                            MentionedCage(ad_id=row.ad_id).update(session)
                            session.commit()
                            status_change = True
                            pass
