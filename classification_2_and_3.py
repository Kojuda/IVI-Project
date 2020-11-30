#!/usr/bin/env python
# coding=utf-8
# author: D.Kohler
# creation: 25.10.2020
# But: classer les oiseaux par leur race

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Classification_2_Ads, Classification_3_Ads, Mapping 
from ressources.regex_tools import mp_mit_egg, mp_mit_2, cage_lexic, birds_lexic, useless_words, egg_lexic, stop_names, too_common_words
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

def re_generator_species() :
    """Create a dictionary {id_species : {common name 1 : regex1, ....}}. These regexes
    will be used to multiples times, so we create them for once for each parsing. We can change
    the code here to adapt the way of create these regexes. The adaption used can be used to create
    different classification. The classification 2 checks the presence of the words of one common name in
    the text. The classification 3 considers the order of the word and the proximity."""
    regex_classification_2={}
    regex_classification_3={}
    for row in session.query(Mapping) :
        #List of common names (stop_names are the common names too general that might match with everything [e.g. Little blue macaw])
        cns = [_.strip(" ") for _ in row.common_name.split(";") if (len(_.strip(" "))>0 and _.strip(" ") not in stop_names)]
        #Add the scientific name
        cns.append(row.scientific_name_cites)
        #List of list of termes included in common names without little words
        cns_decomposed=[[ str.lower(_) for _ in re.split(" |-|'", first) if (len(_)>2)]  for first in cns if (len(first)>0)] #re.split(" -", first)
        #Drop useless words to caracterize a specie (e.g. "and")
        cns_decomposed=[[word for word in l if (word not in useless_words)] for l in cns_decomposed]
        #Drop common bird denomination since several ads don't mention it (it's trivial) (e.g. "parrot")
        #Keep it if there remains only one word
        cns_decomposed=[list(filter(lambda x : x not in too_common_words,l)) if len(list(filter(lambda x : x not in too_common_words,l)))>=2 else l for l in cns_decomposed]
        print(cns_decomposed)
        #Replace each letter with its mitigation in the mitigation dic
        miss_cns=map(lambda list_words : ("".join([mp_mit_2[char] if (char in mp_mit_2.keys())  else char for char in list(word)]) for word in list_words), cns_decomposed)
        #Interpret map object
        miss_cns=[list(_) for _ in list(miss_cns)]
        dict_regex_2 = {}
        dict_regex_3 = {}
        #Populate the dict with regex according to each name
        for name_decomposed, name in zip(miss_cns, cns) :
                #Regex to only find the words in the text. Thus we don't want another letter before to avoid matching "reared" searching for "red"
                reg_2="".join([f"(?=.*[^0-9a-zÀ-ÿ]{word})" for word in name_decomposed])
                reg_2=f"^{reg_2}.*"
                dict_regex_2[name]=reg_2
                #Regex to find the words in a specific order in a specific proximity
                reg_3=".{0,10}".join([f"{word}" for word in name_decomposed])
                reg_3=f"^(?=.*({reg_3})).*"
                dict_regex_3[name]=reg_3

        regex_classification_2[row.id]=(dict_regex_2, row.annex_number_CITES)
        regex_classification_3[row.id]=(dict_regex_3, row.annex_number_CITES)
    return (regex_classification_2, regex_classification_3)

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

def search_re(ad, regexes, classification) :
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
    #appendice of CITES, it is 0 if there is no match
    cites=0
    #Check whether it is a bird
    if re.search(re_isBird, text, re.DOTALL) :
        #cage mentionned or not
        cage=1 if re.search(re_hasCage, text, re.DOTALL) else 0
        #egg is mentionned
        egg=1 if re.search(re_hasEgg, text, re.DOTALL) else 0
        for id_bird in regexes.keys() :
            #regexes[id][0] is the dict of the common names with the regexes
            for regex in regexes[id_bird][0].values() :
                #True at the first match, it's enough.
                result=re.search(regex, text, re.DOTALL)#|re.MULTILINE
                if result :
                    matches+=f";{id_bird}" if (len(matches)>0) else f"{id_bird}"
                    nb_match+=1
                    #Find the corresponding common name according to the regex
                    com_name = [_[0] for _ in regexes[id_bird][0].items() if (regex in _)][0]
                    re_matches[id_bird]=(com_name, regex)

                    #Now for the analysis, with set up a field with the appendice CITES. We assign the worst
                    #appendice for an ad (1 is the worst, so if we have 1 and 2, the appendice will be 1)
                    if regexes[id_bird][1] == 1 :
                        cites=1
                    elif regexes[id_bird][1] == 2 and cites!=1 :
                        cites=2
                    #Special case with the "legal psittaciformes" since there are a few of legal parrots
                    #the definition of CITES is negative for the appendice II. So knowing the only legal parrots
                    #can help to estimate the part of illegal sales.
                    elif regexes[id_bird][1] == -2 and cites!=1 and cites!=2 :
                        cites=-2
                    #Break because we don't need to match all common names, usually only one is used
                    break
                else :
                    pass
    else :
        #No birds => -2
        matches+="-2"
    
    #If not match => -1
    matches="-1" if (len(matches)==0) else matches
    entry=classification(
            ad_id=ad.ad_id,
            ids_matching=matches,
            regex=json.dumps(re_matches),
            nb_species_matches=nb_match,
            cage=cage,
            egg=egg,
            cites_appendice=cites
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

    #2 Dict with regexes for the 2 classifications.
    for dr, classification in zip(dic_regexes, (Classification_2_Ads, Classification_3_Ads)) :
        
        for row in session.query(Parse_ads).filter_by(status_vendeur_taken=0):
            #Skip if already exists
            if session.query(exists().where(classification.ad_id == row.ad_id)).scalar():
                pass
            else:
                entry = search_re(ad=row, regexes=dr, classification=classification)
                print(f"{row.ad_id}...\n")
                doc.addlog(f"Search in ad {row.ad_id}")
                entry.insert(session)
                # row.update(session)


    
        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/classification/documentation/{date_parsing}_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
