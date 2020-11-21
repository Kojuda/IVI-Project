#!/usr/bin/env python
# coding=utf-8
# author: D.Kohler
# creation: 25.10.2020
# But: classer les oiseaux par leur race

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Matching_Ads, Mapping 
from ressources.regex_tools import mp_mit
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))


def re_generator() :
    """Create a dictionary {id_species : {common name 1 : regex1, ....}}. These regexes
    will be used to multiples times, so we create them for once for each parsing. We can change
    the code here to adapt the way of create these regexes."""
    all_birds={}
    for row in session.query(Mapping) :
        id = row.id 
        #List of common names
        cns = [_.strip(" ") for _ in row.common_name.split(";") if (len(_.strip(" "))>0)]
        #List of list of termes included in common names without little words
        cns_decomposed=[[ str.lower(_) for _ in first.split(" ") if (len(_)>2)]  for first in cns if (len(first)>0)]
        #Replace each letter with its mitigation in the mitigation dic
        miss_cns=map(lambda list_words : ("".join([mp_mit[char] if (char in mp_mit.keys())  else char for char in list(word)]) for word in list_words), cns_decomposed)
        #Interpret map object
        miss_cns=[list(_) for _ in list(miss_cns)]
        dict_regex = {}
        #Populate the dict with regex according to each name
        for name_decomposed, name in zip(miss_cns, cns) :
                reg="".join([f"(?=.*{word})" for word in name_decomposed])
                reg=f"^{reg}.*"
                dict_regex[name]=reg
        all_birds[row.id]=dict_regex
    return all_birds

def search_re() :
    pass
if __name__ == '__main__':
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
 
    path_result='./results/calssification/'
    #Vendeur taken en attendant
    for row in session.query(Parse_ads).filter_by(status_vendeur_taken=0):
        #Skip if already exists
        if session.query(exists().where(Parse_ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            dic_regexes=re_generator()
            doc.info["Regexes"]=dic_regexes
            # entry = create_entry(dic_champs, row)

            # session.commit()
            # entry.insert(session)
            # row.update(session)


    
        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/classification/documentation/{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
