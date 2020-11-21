#!/usr/bin/env python
# coding=utf-8
# authors: T. Pineau
# creation: 21.09.2020

import re
# Pour tester les expéressions régulières: https://regex101.com/

def findMails(string):
    '''Récupère des adresses emails dans une chaine de caractère'''
    result = re.findall("\\b[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*(?:[\s\[\(])*(?:@|at)(?:[\s\]\)])*(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", string)
    return result

def findPhones(string):
    '''Récupère des numéros de téléphones suisses de type 079 945 55 11, 0799455511 ou +41 78 545 45 45 avec des espaces, /, - ou concatené'''
    result = re.findall("(\\b(?:\+?41[\s\-/]?)?0?\d{2}[\s\-/]?\d{3}[\s\-/]?\d{2}[\s\-/]?\d{2})", string)
    return result

def findURL(string):
    '''Récupère les URL dans une page (utile lorsque les liens n'ont pas de balises <a href>). Attention, uniquement les liens "HTTP(S) ou www."!'''
    result = re.findall("(\\b(?:HTTP[S]?://|www\.)[\w\d\-\+&@#/%=~_\|\$\?!:,\.]{2,}[\w\d\+&@#/%=~_\|\$]*)", string, re.IGNORECASE)
    return result

def findIPv4(string):
    '''Recherche les adresses IPv4'''
    result = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", string)
    return result

def findIPv6(string):
    '''Recherche les adresses IPv6'''
    result = re.findall("((?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(?:%.+)?\s*", string)
    return result

def removeSpaces(string_or_list):
    '''Supprime des espaces trop nombreux dans une chaine de caractères ou dans une liste de chaine de caractères'''
    if type(string_or_list) == str:
        result = re.sub("\s+", " ", string_or_list).strip() # .strip() permet de supprimer les espaces au début et à la fin de la chaîne
    elif type(string_or_list) == list:
        result = [re.sub('\s+', ' ', string).strip() for string in string_or_list]
    else: result = string_or_list
    return result

def removeTags(string):
    '''Supprime les balises html et ce qu'elles contiennent, privilégier lxml (.text_content()) si de nombreuses balises'''
    result = re.sub("<.*?>", "", string)
    return result

def removeEmptyString(liste):
    '''Supprime des éléments vides dans une liste (passer une liste en argument)'''
    result = [element for element in liste if element] # "if element" est vrai si l'element contient quelque chose. Sinon il n'est pas retourné et est supprimé de la liste
    return result


#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Project REGEX ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Dict of letters with some possibilites of misspelling (Don't consider absence)
mp_mit ={
    "a" : "[Aa4]{1,2}",
    "b" : "[Bb]{1,2}",
    "c" : "[Cc]{1,2}",
    "d" : "[Dd]{1,2}",
    "e" : "[Ee3]{1,2}",
    "f" : "[Ff]{1,2}",
    "g" : "[Gg]{1,2}",
    "h" : "[Hh]{1,2}",
    "i" : "[Ii]{1,2}",
    "j" : "[Jj]{1,2}",
    "k" : "[Kk]{1,2}",
    "l" : "[Ll]{1,2}",
    "m" : "[Mm]{1,2}",
    "n" : "[Nn]{1,2}",
    "o" : "[Oo0]{1,2}",
    "p" : "[Pp]{1,2}",
    "q" : "[Qq]{1,2}",
    "r" : "[Rr]{1,2}",
    "s" : "[Ss]{1,2}",
    "t" : "[Tt]{1,2}",
    "u" : "[Uu]{1,2}",
    "v" : "[Vv]{1,2}",
    "w" : "[Ww]{1,2}",
    "x" : "[Xx]{1,2}",
    "y" : "[Yy]{1,2}",
    "z" : "[Zz]{1,2}"
}

mp_mit_2 ={
    "a" : "[a]{1,2}",
    "b" : "[b]{1,2}",
    "c" : "[c]{1,2}",
    "d" : "[d]{1,2}",
    "e" : "[e]{1,2}",
    "f" : "[f]{1,2}",
    "g" : "[g]{1,2}",
    "h" : "[h]{1,2}",
    "i" : "[i]{1,2}",
    "j" : "[j]{1,2}",
    "k" : "[k]{1,2}",
    "l" : "[l]{1,2}",
    "m" : "[m]{1,2}",
    "n" : "[n]{1,2}",
    "o" : "[o]{1,2}",
    "p" : "[p]{1,2}",
    "q" : "[q]{1,2}",
    "r" : "[r]{1,2}",
    "s" : "[s]{1,2}",
    "t" : "[t]{1,2}",
    "u" : "[u]{1,2}",
    "v" : "[v]{1,2}",
    "w" : "[w]{1,2}",
    "x" : "[x]{1,2}",
    "y" : "[y]{1,2}",
    "z" : "[z]{1,2}"
}

cage_lexic=["cage", "jail", "enclosure", "cabine", "trap"]
birds_lexic=["bird", "macaw", "amazon", "parrot", "parakeet", "macaw", "ara", "cacato", "perruche","kakapo", "cockatoo", "lorikeet", "lori", "african grey", "conure"]
bird_denominations=["parrot"]