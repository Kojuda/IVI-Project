#!/usr/bin/env python
# coding=utf-8
# author: L. RodJ.Wyss
# creation: 13.11.2020
# But: parser le code client des publications de vente

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation
from ressources.db import session, Parse_ads, Parsing_Psittaciformes_or_no, Mapping
from spelling_error_mitigation import word_to_regex
list_scientific = []

#transformer table mapping_names en REGEX
for row in session.query(Mapping):
    # traitement scientific name
    a = word_to_regex(row.scientific_name_cites)
    list_scientific.append(a)
    #traitement common name
    entree = row.common_name.split(';') #creer la list
    for name in entree:
        if (name == '')or(name == ' '):
            pass
        try:
            list = name.split(' ')
            print(list)

            list.del('Amazone')
            list.del('')
            print(list)
        except:
            pass

    print(entree)






if __name__ == '__main__':
    path_result = './results/parse/'
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    #parse database
    c = 0 #counter to trace vow many ads have status 1 = classified as bird
    #for row in session.query(Parse_ads):
