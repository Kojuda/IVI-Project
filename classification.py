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

def search_re(ad, regexes) :
    """For each ad, we search with the regexes in the breed, title and description fields to
    find one common name of a bird in the CITES mapping. The text is analyzed with each regex common name
    from each birds. If a common name is matched, it passes to the next bird. No need to match several common
    names."""
    #We add the fields in this order to start with the fields that most likely contain the name
    #to stop as fast as possible to earn computational time
    text=f"{ad.breed} {ad.title} {ad.description}"
    #String with all the id_birds that have matched with ";" separator
    matches=""
    #Dict containing the matching regex with the bird_id and the common name
    re_matches={}
    #number of matches
    nb_match=0
    for id_bird in regexes.keys() :
        for regex in regexes[id_bird].values() :
            cp_re=re.compile(regex)
            #True at the first match, it's enough
            result=cp_re.search(text, re.DOTALL|re.MULTILINE)
            if result :
                matches+=f";{id_bird}"
                nb_match+=1
                #Find the corresponding common name according to the regex
                com_name = [_[0] for _ in re_matches[id_bird].items() if (regex in _)][0]
                re_matches[id_bird]=(com_name, regex)
                #Break because we don't need to match all common names, usually only one is used
                break
            else :
                pass

    entry=Matching_Ads(
            ad_id=ad.ad_id,
            ids_matching=matches,
            regex=json.dumps(re_matches, indent=4),
            nb_species_matches=nb_match
    )
    return entry

if __name__ == '__main__':
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
 
    path_result='./results/calssification/'
    #Vendeur taken en attendant


    #~~~~~~~~~~~~~~ Create Regexes ~~~~~~~~~~~~~~
    dic_regexes=re_generator()
    doc.info["Regexes"]=dic_regexes
    doc.addlog("Create regexes")


    for row in session.query(Parse_ads).filter_by(status_vendeur_taken=0):
        #Skip if already exists
        if session.query(exists().where(Parse_ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            entry = search_re(ad=row, regexes=dic_regexes)
            doc.addlog[f"Search in ad {row.ad_id}"]

            session.commit()
            entry.insert(session)
            # row.update(session)


    
        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/classification/documentation/{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
