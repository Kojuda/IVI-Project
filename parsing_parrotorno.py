#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues, J.Wyss
# creation: 20.11.2020
# But: parmis les oiseaux, psittaciformes (plupart perroquets) ou pas?

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_Psittaciformes_or_no, Parsing_bird_or_no, Mapping, Regex, Match_Regex_IdMap
from spelling_error_mitigation import word_to_regex
list_scientific = []
status_modified = False #A changer à true si changé spelling erreur mitigation ou table cites + supprimer tables

#transformer table mapping_names en REGEX if modifications were made [aliments tables regex et match_regex_idmap
if status_modified:
    for row in session.query(Mapping):
        #print(row.id)
    # traitement scientific name
        a = word_to_regex(row.scientific_name_cites)
        list_scientific.append(a)
        # traitement common name
        entree = row.common_name.split('; ') #créer la liste
        for name in entree:
            name.lower()
            list_of_words = name.split(' ')
            for i in list_of_words:
                if len(i) < 3: #let alone small words
                    pass
                else: #big words - we do something with them: namely
                    if type(i)==str: #check if string, if not string we just sit idle
                        res = word_to_regex(i)
                    else:
                        print('problem with input')
                        res = False
                    if session.query(Regex).filter(Regex.reg==res).scalar()==None: #if entry doesn't exist: create entry in regex database
                        entry = Regex(reg=res)
                        entry.insertregex(session)
                        session.commit()
                    else: #if no entry pass
                        pass
                    #now we fillup  Match_Regex_IdMap
                    requested_re = session.query(Regex.id).filter(Regex.reg==res)
                    request = session.query(Match_Regex_IdMap.id).filter_by(id_re=requested_re, id_map=row.id).scalar()
                    if request==None:
                        entry = Match_Regex_IdMap(id_re=requested_re, id_map=row.id)
                        entry.insertMatch(session)
                        session.commit()


if __name__ == '__main__':
    #générer list_scientific
    for row in session.query(Mapping):
        a = word_to_regex(row.scientific_name_cites)
        list_scientific.append(a)

    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()


    #SCIENTIFIC: parse database
    #connexion = session.query(Mapping.id).scalar()
    #print(connexion)
    #mapping_match_1=mapping_cites.id

    # c = 0 #counter to trace vow many ads have status 1 = classified as psittaciforme
    for row in session.query(Parse_ads):
        if session.query(Parsing_bird_or_no).filter_by(status_bird=1, ad_id=row.ad_id).scalar() != None:
            if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None:
        #         print('no entry')
        #NOM SCIENTIFIQUE
        #         # step 1 search in title
                match_scientific = 0 #default pas de match
                if match_scientific == 0:
                    for expression in list_scientific:
        #             # For each defined regular expression
                        res = re.search(expression, row.title)
                        if res!= None:
                            match_scientific = 1
                        if row.description != None:
                            res_des = re.search(expression,row.description)
                            if res_des!= None:
                                match_scientific = 1
                    #if match_scientific == 1:
                        #print(match_scientific, row.ad_id)

                match_common = 0 #default pas de match
                list_match_common = []
                for regex in session.query(Regex):
                    try:
                        res_titre = re.search(regex.reg, row.title)
                        if res_titre != None:
                            match_common = 1
                            if str(regex.id) not in list_match_common:
                                list_match_common.append(str(regex.id))
                    except:
                        print('error in re_titre')
                    try:
                        res_description = re.search(regex.reg, row.description)
                        if res_description != None:
                            match_common = 1
                            if str(regex.id) not in list_match_common:
                                list_match_common.append(str(regex.id))
                    except:
                        print('error in res_description')
                #print(row.ad_id, match_common, list_match_common)

                separator = ';'
                try:
                    lmc = separator.join(list_match_common) #dans spelling_error_mitigation separator.join(l)
                #print(lmc)
                except:
                    print('error lmc empty')
                    lmc = None
                entry = Parsing_Psittaciformes_or_no(ad_id=row.ad_id, match_cites_parrot=match_scientific, match_common_parrot=match_common, mapping_match=lmc)
                entry.insertPsittaciformes(session)
                session.commit()
