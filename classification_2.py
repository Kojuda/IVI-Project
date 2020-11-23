#!/usr/bin/env python
# coding=utf-8
# author: D.Kohler
# creation: 25.10.2020
# But: classer les oiseaux par leur race

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Matching_Ads, Mapping 
from ressources.regex_tools import mp_mit_egg, mp_mit_2, cage_lexic, birds_lexic, bird_denominations, egg_lexic
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

def re_generator_species() :
    """Create a dictionary {id_species : {common name 1 : regex1, ....}}. These regexes
    will be used to multiples times, so we create them for once for each parsing. We can change
    the code here to adapt the way of create these regexes."""
    all_birds={}
    for row in session.query(Mapping) :
        id = row.id 
        #List of common names
        cns = [_.strip(" ") for _ in row.common_name.split(";") if (len(_.strip(" "))>0)]
        #Add the scientific name
        cns.append(row.scientific_name_cites)
        #List of list of termes included in common names without little words
        cns_decomposed=[[ str.lower(_) for _ in re.split(" |-|'", first) if (len(_)>2)]  for first in cns if (len(first)>0)] #re.split(" -", first)
        #Drop common bird denomination since several ads don't mention it (it's trivial) (e.g. "parrot")
        cns_decomposed=[[word for word in l if (word not in bird_denominations)] for l in cns_decomposed]
        print(cns_decomposed)
        #Replace each letter with its mitigation in the mitigation dic
        miss_cns=map(lambda list_words : ("".join([mp_mit_2[char] if (char in mp_mit_2.keys())  else char for char in list(word)]) for word in list_words), cns_decomposed)
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

def re_isBird() :
    """Create a regex according to a dictionnary that will signal the presence of a word
    of this lexic in a text"""
    #Replacement that tolerate misspelling
    miss_bird=["".join([mp_mit_2[char] if (char in mp_mit_2.keys())  else char for char in list(word)]) for word in birds_lexic]
    #A regex that matches only if one of bird_lexic word is present
    reg=f"^(?=.*{'|.*'.join(miss_bird)}).*"
    return reg

def re_hasCage() :
    """Create a regex according to a dictionnary that will signal the presence of a word
    of this lexic in a text"""
    #Replacement that tolerate misspelling
    miss_cage=["".join([mp_mit_2[char] if (char in mp_mit_2.keys())  else char for char in list(word)]) for word in cage_lexic]
    #A regex that matches only if one of cage_lexic word is present
    reg=f"^(?=.*{'|.*'.join(miss_cage)}).*"
    return reg

def re_hasEgg() :
    """Create a regex according to a dictionnary that will signal the presence of a word
    of this lexic in a text"""
    #Replacement that tolerate misspelling
    miss_egg=["".join([mp_mit_egg[char] if (char in mp_mit_egg.keys())  else char for char in list(word)]) for word in egg_lexic]
    #A regex that matches only if one of cage_lexic word is present
    #Avoid "veggies" and a space to avoid all words like "eggplant"
    reg=f"^(?=.*{' |.*[^v]'.join(miss_egg)}).*"
    return reg

def search_re(ad, regexes) :
    """For each ad, we search with the regexes in the breed, title and description fields to
    find one common name of a bird in the CITES mapping. The text is analyzed with each regex common name
    from each birds. If a common name is matched, it passes to the next bird. No need to match several common
    names."""
    #We add the fields in this order to start with the fields that most likely contain the name
    #to stop as fast as possible to earn computational time. (lower reduces variability)
    text=f"{ad.breed} {ad.title} {ad.description}".lower()
    #String with all the id_birds that have matched with ";" separator
    matches=""
    #Dict containing the matching regex with the bird_id and the common name
    re_matches={}
    #number of matches
    nb_match=0
    #cage mentionned (-1 = no check)
    cage=-1
    #egg is mentioned (-1 no check)
    egg=-1
    #Check whether it is a bird
    if re.search(re_isBird, text, re.DOTALL) :
        #cage mentionned or not
        cage=1 if re.search(re_hasCage, text, re.DOTALL) else 0
        #egg is mentionned
        egg=1 if re.search(re_hasEgg, text, re.DOTALL) else 0
        for id_bird in regexes.keys() :
            for regex in regexes[id_bird].values() :
                #True at the first match, it's enough
                result=re.search(regex, text, re.DOTALL)#|re.MULTILINE
                if result :
                    matches+=f";{id_bird}" if (len(matches)>0) else f"{id_bird}"
                    nb_match+=1
                    #Find the corresponding common name according to the regex
                    com_name = [_[0] for _ in regexes[id_bird].items() if (regex in _)][0]
                    re_matches[id_bird]=(com_name, regex)
                    #Break because we don't need to match all common names, usually only one is used
                    break
                else :
                    pass
    else :
        #No birds => -2
        matches+="-2"
    
    #If not match => -1
    matches="-1" if (len(matches)==0) else matches
    entry=Matching_Ads(
            ad_id=ad.ad_id,
            ids_matching=matches,
            regex=json.dumps(re_matches),
            nb_species_matches=nb_match,
            cage=cage,
            egg=egg
    )
    return entry

#GLOBAL (regexes)
re_hasCage=re_hasCage()
re_isBird=re_isBird()
re_hasEgg=re_hasEgg()

if __name__ == '__main__':
    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
 
    path_result='./results/calssification/'
    #Vendeur taken en attendant


    #~~~~~~~~~~~~~~ Create Regexes ~~~~~~~~~~~~~~
    dic_regexes=re_generator_species()
    doc.info["regexes"]=dic_regexes
    doc.addlog("Create regexes")
    doc.info["cage_regex"]=re_hasCage
    doc.info["isbird_regex"]=re_isBird


    for row in session.query(Parse_ads).filter_by(status_vendeur_taken=0):
        #Skip if already exists
        if session.query(exists().where(Matching_Ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            entry = search_re(ad=row, regexes=dic_regexes)
            print(f"{row.ad_id}...\n")
            doc.addlog(f"Search in ad {row.ad_id}")

            entry.insert(session)
            # row.update(session)


    
        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/classification/documentation/{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
