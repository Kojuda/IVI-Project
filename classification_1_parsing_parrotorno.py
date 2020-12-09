#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues, J.Wyss
# creation: 20.11.2020
# But: parmis les oiseaux, psittaciformes (plupart perroquets) ou pas?

"""Ce script fait partie de la première classification. Il permet d'établir la liste des mots recherchés
dans une annonce et d'établir si ces mots font partie du lexique concernant les psittaciforems et/ou si
ces mots font parties du lexique des espèces CITES de la table "mapping_cites". Les données sont stockées
dans la table "classification_1_psittaciformes_or_no" (matches par annonce), "classification_1_regex" 
(expressions régulières utilisées lors du script) et "classification_1_reg_map_match" (correspondance 
entre une expression régulière/mot et une espèce de la table "mapping_cites") """

import re, datetime
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_Psittaciformes_or_no, Parsing_bird_or_no, Mapping, Regex, Match_Regex_IdMap
from ressources.regex_tools import word_to_regex
list_scientific = []
status_modified = False #Changer en True si regex_tools ou table mapping_cites changés + supprimer tables


def make_dictionnary():
    """Creates dictionnary for small multiple (Script classification_1_visualisation), this dictonary contains the words corresponding to the regex used for classification 1"""
    result_dict = {}
    for row in session.query(Mapping): #for each ligne in table mapping
        result = [] #temporary list
        #add scientific name
        result.append(row.scientific_name_cites.lower()) #append scientific name to list
        #add common names
        entry = row.common_name.split('; ')  #create a list with each common name as an entry
        for name in entry: #for each name in the list created in the previous line
            name.lower() #get all letters to lowercase
            list_of_words = name.split(' ') #split the common name into it's components [this creates again a list]
            for i in list_of_words: #for each entry given here
                try:
                    res = word_to_regex(i) #try to make a regular expression from the word
                except:
                    res = None
                if len(i) <= 2: #let alone small words
                    pass
                elif len(i) < 5 and (('\s' in res) or ('\w' in res) or (res == '')): #if there is a problem in the creation of the word, let it alone
                    #and with problem are ment words smaller than 5 letters containing space caracters, commonplace caracters or empty fields
                    pass
                else: #big words - we do something with them: namely
                    if type(i)==str: #check if string, if not string we just sit idle
                        if res != None:
                            result.append(i.lower().strip(';')) #append lower case result without ';'
        result_dict[row.id]=result #for each entry in mapping append the list of used words
    return result_dict #return dictionary

#transformer table mapping_names en REGEX if modifications were made [aliments tables regex et match_regex_idmap
def make_helper_tables():
    """creates regex table, regex_id map table
        basically creates the tables used later for reconstruction the matches
        they don't contain the scientific names"""
    for row in session.query(Mapping): #for each entry in the table mapping_cites
        # traitement common name
        entree = row.common_name.split('; ') #create list with common names as entries
        for name in entree: #for each common name
            name.lower() #get letters to be in lowercase
            list_of_words = name.split(' ') #create the a list of the words composing the common name
            for i in list_of_words:
                if len(i) <= 2: #let alone small words
                    pass
                else: #big words - we do something with them: namely
                    if type(i)==str: #check if string, if not string we just sit idle
                        res = word_to_regex(i)
                    else:
                        print('problem with input')
                        res = None
                    if len(i)<5: #for small words we have additional requirements before they are added to the list
                        if ('\s' in res) or ('\w' in res) or (res==''):
                            print('exception, pass short error', res)
                            res = None
                        else:
                            if session.query(Regex).filter(Regex.reg==res).scalar()==None and res!= None: #if there isn't already an entry and the regex isn't problematic
                                entry = Regex(reg=res, word=word.lower().strip(';')) #create entry
                                entry.insertregex(session) #insert entry
                                session.commit() #commit entry
                    #for long words len>=5
                    elif session.query(Regex).filter(Regex.reg==res).scalar()==None and res!= None: #if entry doesn't exist: create entry in regex database
                        word=i.strip(';')
                        entry = Regex(reg=res, word=word.lower().strip(';'))
                        entry.insertregex(session)
                        session.commit()
                    else: #if no entry pass
                        pass
                    #next step: fillup  Match_Regex_IdMap
                    requested_re = session.query(Regex.id).filter(Regex.reg==res).scalar()
                    request = session.query(Match_Regex_IdMap.id).filter_by(id_re=requested_re, id_map=row.id).scalar()
                    if request==None and requested_re!=None: #if there isn't an entry (request) and the regular_expression exists in Regex (requested_re)
                        entry = Match_Regex_IdMap(id_re=requested_re, id_map=row.id)  #create entry
                        entry.insertMatch(session) #insert
                        session.commit() #commit

if __name__ == '__main__':
    if status_modified: #if we changed something with the generation of regexes or the mapping table
        make_helper_tables() #regenerate helper tables
    res = make_dictionnary()
    #générer list_scientific
    for row in session.query(Mapping):
        a = word_to_regex(row.scientific_name_cites)
        list_scientific.append(a)

    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()

    #create entries for Parsing_Psittasiformes (one per ad)
    #the match_scientific and match_common only take values either 1 (match found) or 0 (match not found)
    #list_common lists all the regular expressions found
    for row in session.query(Parse_ads): #for each parsed ad
        if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(ad_id=row.ad_id).scalar() == None: #if there isn't already an entry in Parsing_psittasiformes
        #NOM SCIENTIFIQUE: search if the scientific name is mentioned
                # step 1 search in title, description and breed
            match_scientific = 0 #default pas de match
            for expression in list_scientific: #search all scientific names
                if match_scientific == 0: # if we didn't find a match yet get to next
                    # For each defined regular expression
                    res_tit = re.search(str(expression), row.title)
                    if res_tit != None: #if the scientific name was found in the title
                        match_scientific = 1 #change match_scientific to 1
                    if row.description != None: #if there is a description
                        res_des = re.search(str(expression),row.description)
                        if res_des!= None: #if the regex matched in the description
                            match_scientific = 1 #change match_scientific to 1
                    if row.breed != None: #if a breed is specified
                        res_bre = re.search(str(expression), row.breed)
                        if res_bre != None: #if the regex matched in the field breed
                            match_scientific = 1 #change match_scientific to 1

        #NOM COMMUN
            match_common = 0 #default no match
            list_match_common = [] #default no matching common name regex
            for regex in session.query(Regex): #for each regular expression in the constructed helper table
                #search given regex in title of the ad
                try:
                    res_title = re.search(regex.reg, row.title) #search title for the expression
                    if res_title != None: #if there is a result
                        match_common = 1 #change match status
                        if str(regex.id) not in list_match_common:
                            list_match_common.append(str(regex.id)) #append word to list_match_common if not already in list
                except:
                    print('error in res_title - no title for ad found (?)')
                #search given regex in description
                try:
                    res_description = re.search(regex.reg, row.description)
                    if res_description != None:
                        match_common = 1
                        if str(regex.id) not in list_match_common:
                            list_match_common.append(str(regex.id))
                except:
                    print('error in res_description - no description found')
                #search given regex in breed field
                try:
                    res_breed = re.search(regex.reg, row.breed)
                    if res_breed != None:
                        match_common = 1
                        if str(regex.id) not in list_match_common:
                            list_match_common.append(str(regex.id))
                except:
                        print('error in res_breed - no breed found')

            separator = ';'
            try:
                lmc = separator.join(list_match_common) #try to create string where the id of the regex are separeted by ;
            except:
                print('error in lmc creation - lmc empty')
                lmc = None
            entry = Parsing_Psittaciformes_or_no(ad_id=row.ad_id, match_cites_parrot=match_scientific, match_common_parrot=match_common, mapping_match=lmc)
            entry.insertPsittaciformes(session)
            session.commit()
        #documentation:
        with open(f'./results/classification/documentation/parrot_{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))