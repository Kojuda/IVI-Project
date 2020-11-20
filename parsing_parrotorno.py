#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues, J.Wyss
# creation: 20.11.2020
# But: parmis les oiseaux, psittaciformes (plupart perroquets) ou pas?

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_Psittaciformes_or_no, Mapping, Regex, Match_Regex_IdMap
from spelling_error_mitigation import word_to_regex
list_scientific = []
status_modified = False

#transformer table mapping_names en REGEX if modifications were made [aliments tables regex et match_regex_idmap
if status_modified:
    for row in session.query(Mapping):
    print(row.id)
    # traitement scientific name
    a = word_to_regex(row.scientific_name_cites)
    list_scientific.append(a)
    # traitement common name
    entree = row.common_name.split('; ') #créer la liste
    for name in entree:
        #if (name == '')or(name == ' '):
        #    pass
        #print(name)
        # try:
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
                request=session.query(Regex.id).filter(Regex.reg==res).scalar()
                if request!=None:
                    entry = Match_Regex_IdMap(id_re=request, id_map=row.id)
                    entry.insertMatch(session)
                    session.commit()








        #Il faudra quand même mettre quelque part Parrot, Parakeet, Amazon, Psittacus, etc. pour
        #PARROT OR NO, mais pour la race spécifique c'est mieux d'enlever:
        #Aussi problème de couleur (chaque green est trouvé p. ex.) et problème de type (Amazone, Macaw, Cockatoo):
        #Toujours plusieurs races comprenant ces noms, mais parfois la personne va juste écrire "Amazone" ou "Cockatoo" sans préciser
        #Et si on enlève on ne trouvera jamais....
        # while 'Amazon' in list:
        #     list.remove('Amazon')
        # while 'Amazone' in list:
        #     list.remove('Amazone')
        # while 'Amazona' in list:
        #     list.remove('Amazona')
        # while 'Psittacus' in list:
        #     list.remove('Psittacus')
        # while 'Parrot' in list:
        #     list.remove('Parrot')
        # while 'parrot' in list:
        #     list.remove('parrot')
        # while 'parakeet' in list:
        #     list.remove('parakeet')
        # while 'Parakeet' in list:
        #     list.remove('Parakeet')
        # while 'Macaw' in list:
        #     list.remove('Macaw')
        # while 'macaw' in list:
        #     list.remove('macaw')
        # while 'de' in list:
        #     list.remove('de')
        # while 'des' in list:
        #     list.remove('des')
        # while 'le' in list:
        #     list.remove('le')
        # while 'la' in list:
        #     list.remove('la')
        # while 'à' in list:
        #     list.remove('à')
        # while '' in list:
        #     list.remove('')
        # print(list)
        # except:
        #     pass


# TODO: mettre qqch pour que ce soit case non-sensitive si pas déjà fait?



if __name__ == '__main__':
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
    # for row in session.query(Parse_ads):
    #     if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None:
    #         print('no entry')
    #
    #         # step 1 search in title
    #         for expression in list_scientific:
    #             # For each defined regular expression
    #             res = re.search(expression, row.title)  # search in title
    #             if res != None:  # if there is a match, go on
    #                 if session.query(Parsing_Psittaciformes_or_no.match_cites_parrot).filter_by(ad_id=row.ad_id).scalar() == None:  # if there isn't already an entry
    #                     entry = Parsing_Psittaciformes_or_no(ad_id=row.ad_id, match_cites_parrot=1)
    #                     entry.insertPsittaciformes(session)
    #                     session.commit()
    #                     c += 1
    #                     pass
    #
    #
    #         # step 2 search in description
    #         for expression in list_scientific:
    #             if row.description != None:
    #                 try:
    #                     res = re.search(expression, row.description)
    #                 except:
    #                     print('unknown error')
    #                     print(row.ad_id)
    #                     res = None
    #             if res != None:
    #                 if session.query(Parsing_Psittaciformes_or_no.match_cites_parrot).filter_by(ad_id=row.ad_id).scalar() == None:
    #                     print('description')
    #                     entry = Parsing_Psittaciformes_or_no(ad_id=row.ad_id, match_cites_parrot=1)
    #                     entry.insertPsittaciformes(session)
    #                     session.commit()
    #                     pass
    #
    #         # last step if no match add status 0
    #         # if session.query(Parsing_Psittaciformes_or_no.match_cites_parrot).filter_by(ad_id=row.ad_id).scalar()
    #         if session.query(Parsing_Psittaciformes_or_no.match_cites_parrot).filter_by(ad_id=row.ad_id).scalar() == None:
    #             entry = Parsing_Psittaciformes_or_no(ad_id=row.ad_id, match_cites_parrot=0)
    #             entry.insertPsittaciformes(session)
    #             session.commit()
    #
    #     else:
    #         print('entry exists')
    #         #print(session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar(), type(session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()))
    #         if session.query(Parsing_Psittaciformes_or_no.match_cites_parrot).filter_by(ad_id=row.ad_id).scalar()==0:
    #             print('change')
    #             status_change = False
    #             # step 1 search in title
    #             for expression in list_scientific:
    #                 # For each defined regular expression
    #                 res = re.search(expression, row.title)  # search in title
    #                 if res != None:  # if there is a match, go on
    #                     if status_change:
    #                         print('change stat')
    #                         Parsing_Psittaciformes_or_no(ad_id=row.ad_id).update(session)
    #                         session.commit()
    #                         c += 1
    #                         status_change = True
    #                         pass
    #                 try:
    #                     res_des = re.search(expression, row.description)
    #                     print(res_des.scalar()) #déplacé
    #                 except:
    #                     res_des = None
    #                 if res_des != None:
    #                     if status_change:
    #                         print('change des')
    #                         Parsing_Psittaciformes_or_no(ad_id=row.ad_id).update(session)
    #                         session.commit()
    #                         c += 1
    #                         status_change = True
    #                         pass
