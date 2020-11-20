#!/usr/bin/env python
# coding=utf-8
# author: D.Kohler
# creation: 25.10.2020
# But: classer les oiseaux par leur race

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Matching_Ads, Mapping 
from ressources.regex_tools import misspelling_mitigations


def re_generator() :
    for row in session.query(Mapping) :
        id = row.id 
        #List of common names
        cns = [_.strip(" ") for _ in row.common_name.split(";")]
        #List of list of termes included in common names without little words
        cns_decomposed=[[ str.lower(_) for _ in first.split(" ") if (len(_)>2)]  for first in cns if (len(first)>0)]

        
    #create a dictionary {id_species : {common name 1 : regex1, ....}}

def search_re() :
    pass
if __name__ == '__main__':
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
 
    path_result='./results/getCodes/codes/'

    for row in session.query(Ads_Codes).filter_by(status=0):
        #Skip if already exists
        if session.query(exists().where(Parse_ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            dic_champs=dict_champ.copy()
            filename=row.client_code
            dic_champs["Ad Number"]=row.ad_number
            objet = lxml.html.parse(f"{path_result}{filename}").getroot()
            dic_champs = get_champs(dic_champs, objet, doc)
            entry = create_entry(dic_champs, row)

            session.commit()
            entry.insertParse_ads(session)
            row.update(session)


    #before: f'./results/parseCodes/documentation/
    # for jasmin: f'C:/Users/Jasmin/Documents/Switchdrive/results/getCodes/documentation/'
        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/parseCodes/documentation/{date_parsing}_documentation.json', 'wb') as f:
                    f.write(str(doc).encode('utf-8'))
