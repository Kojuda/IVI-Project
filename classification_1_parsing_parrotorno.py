#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues, J.Wyss
# creation: 20.11.2020
# But: parmis les oiseaux, psittaciformes (plupart perroquets) ou pas?

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_Psittaciformes_or_no, Parsing_bird_or_no, Mapping, Regex, Match_Regex_IdMap
from ressources.regex_tools import word_to_regex
list_scientific = []
status_modified = True #Changer en True si regex_tools ou table mapping_cites changés + supprimer tables

#transformer table mapping_names en REGEX if modifications were made [aliments tables regex et match_regex_idmap
def make_helper_tables():
    """creates regex table, regex_id map table """
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
                if len(i) <= 2: #let alone small words
                    pass
                else: #big words - we do something with them: namely
                    if type(i)==str: #check if string, if not string we just sit idle
                        res = word_to_regex(i)
                    else:
                        print('problem with input')
                        res = None
                    if len(i)<5:
                        if ('\s' in res) or ('\w' in res) or (res==''):
                            print('exception, pass short error', res)
                            res = None
                        else:
                            if session.query(Regex).filter(Regex.reg==res).scalar()==None and res!= None:
                                word=i.strip(';')
                                entry = Regex(reg=res, word=word)
                                entry.insertregex(session)
                                session.commit()
                    elif session.query(Regex).filter(Regex.reg==res).scalar()==None and res!= None: #if entry doesn't exist: create entry in regex database
                        word=i.strip(';')
                        entry = Regex(reg=res, word=word)
                        entry.insertregex(session)
                        session.commit()
                    else: #if no entry pass
                        pass
                    #now we fillup  Match_Regex_IdMap
                    requested_re = session.query(Regex.id).filter(Regex.reg==res).scalar()
                    request = session.query(Match_Regex_IdMap.id).filter_by(id_re=requested_re, id_map=row.id).scalar()
                    if request==None and requested_re!=None:
                        entry = Match_Regex_IdMap(id_re=requested_re, id_map=row.id)
                        entry.insertMatch(session)
                        session.commit()

def make_dictionnary():
    """creates dictionnary for small multiple"""
    result_dict = {}
    for row in session.query(Mapping):
        result = []
        #add scientific name
        result.append(word_to_regex(row.scientific_name_cites))
        #add common names
        entry = row.common_name.split('; ')
        for name in entry:
            name.lower()
            list_of_words = name.split(' ')
            for i in list_of_words:
                try:
                    res = word_to_regex(i)
                except:
                    res = None
                if len(i) <= 2: #let alone small words
                    pass
                elif len(i) < 5 and (('\s' in res) or ('\w' in res) or (res == '')):
                    pass
                else: #big words - we do something with them: namely
                    if type(i)==str: #check if string, if not string we just sit idle
                        if word_to_regex(i) not in result:
                            result.append(res)
        result_dict[row.id]=result
    return result_dict




if __name__ == '__main__':
    if status_modified:
        make_helper_tables()
    res = make_dictionnary()
    print(res)
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
        #if session.query(Parsing_bird_or_no).filter_by(status_bird=1, ad_id=row.ad_id).scalar() != None:
        if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None:
        #         print('no entry')

        #NOM SCIENTIFIQUE
                # step 1 search in title, description and breed
                match_scientific = 0 #default pas de match
                if match_scientific == 0:
                    for expression in list_scientific:
                        # For each defined regular expression
                        res_tit = re.search(str(expression), row.title)
                        if res_tit != None:
                            match_scientific = 1
                        if row.description != None:
                            res_des = re.search(str(expression),row.description)
                            if res_des!= None:
                                match_scientific = 1
                        if row.breed != None:
                            res_bre = re.search(str(expression), row.breed)
                            if res_bre != None:
                                match_scientific = 1

        #NOM COMMUN
                match_common = 0 #default pas de match
                list_match_common = []
                for regex in session.query(Regex):
                    try:
                        res_title = re.search(regex.reg, row.title)
                        if res_title != None:
                            match_common = 1
                            if str(regex.id) not in list_match_common:
                                list_match_common.append(str(regex.id))
                    except:
                        print('error in res_title')

                    try:
                        res_description = re.search(regex.reg, row.description)
                        if res_description != None:
                            match_common = 1
                            if str(regex.id) not in list_match_common:
                                list_match_common.append(str(regex.id))
                    except:
                        print('error in res_description')

                    try:
                        res_breed = re.search(regex.reg, row.breed)
                        if res_breed != None:
                            match_common = 1
                            if str(regex.id) not in list_match_common:
                                list_match_common.append(str(regex.id))
                    except:
                        print('error in res_breed')

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
        with open(f'./results/classification/documentation/parrot_{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))