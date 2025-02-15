#!/usr/bin/env python
# coding=utf-8
# authors: T. Pineau
# creation: 21.09.2020

"""
Ressources fournissant des functions utiles pour l'ensemble des travaux sur les expressions régulières. De plus, 
l'ensemble des lexiques et dictionnaires utilisés pour générer les expressions régulières pour transformer
des caractères dans une chaîne sont stockés dans ce module.
Il y a deux manières de construire des regex fournit
"""

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

def word_to_regex(word: str):
    """function used by parse_birds and parse_parrot, basically trasforms a given word into a regular expression, needs a string in input"""
    l = [] #create empty list
    separator='' #space caracter in string used to seperate words
    for i in range(0, len(word)): #for every caracter of the given word
        if i==';': # if the caracter is an ';' sit idle
            pass
        else:
            try:
                l.append('('+dict_alphabet[word[i].lower()]+'){1}') #try to trasform a given charachter into a a group in the regular expression
            except:
                # if this didn't work (as in the character isn't in the dictionnary)
                if len(l)>4: #if the word is long enough, we append simply \w (any word caracter)
                    l.append('(\w){0,1}')
                #else: sit idle
    res = separator.join(l) #merge all groups together
    return res #return the regular expression

#Dict of letters with some possibilites of misspelling (Don't consider absence)
mp_mit_egg ={
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
    "o" : "[o0]{1,2}",
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
    "z" : "[z]{1,2}",
    "è" : "[èéêe]{1,2}",
    "é" : "[èéêe]{1,2}",
    "à" : "[àaá4]{1,2}",
    "á" : "[àaá4]{1,2}",
    "ç" : "[çc]{1,2}",
    "ú" : "[úùûüu]{1,2}",
    "å" : "[ãåàaá]{1,2}",
    "ã" : "[ãåàaá]{1,2}",
    "ù" : "[úùûüu]{1,2}",
    "ê" : "[èéêe]{1,2}",
    "(" : "",
    ")" : ""
}
#Dict of letters with some possibilites of misspelling (Don't consider absence)
mp_mit_2 ={
    "a" : "[ae4]{1,2}", #grey
    "b" : "[b]{1,2}",
    "c" : "[c]{1,2}",
    "d" : "[d]{1,2}",
    "e" : "[ea3]{1,2}", #gray
    "f" : "[f]{1,2}",
    "g" : "[g]{1,2}",
    "h" : "[h]{1,2}",
    "i" : "[i]{1,2}",
    "j" : "[j]{1,2}",
    "k" : "[k]{1,2}",
    "l" : "[l]{1,2}",
    "m" : "[m]{1,2}",
    "n" : "[n]{1,2}",
    "o" : "[o0]{1,2}",
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
    "z" : "[z]{1,2}",
    "è" : "[èéêe]{1,2}",
    "é" : "[èéêe]{1,2}",
    "à" : "[àaá4]{1,2}",
    "á" : "[àaá4]{1,2}",
    "ç" : "[çc]{1,2}",
    "ú" : "[úùûüu]{1,2}",
    "å" : "[ãåàaá]{1,2}",
    "ã" : "[ãåàaá]{1,2}",
    "ù" : "[úùûüu]{1,2}",
    "ê" : "[èéêe]{1,2}",
    "ï" : "[iïíì]{1,2}",
    " " : " ",
    "(" : "",
    ")" : ""
}

#dict_alphabet is used for the first classification (parse_birdorno /parse_parrotorno)
#in the dictionary the inside of a group is defined
dict_alphabet = {}
dict_alphabet['a']='à+|á+|a+|A+|4+'
dict_alphabet['b']='b+|B+'
dict_alphabet['c']='c+|C+|ç+'
dict_alphabet['d']='d+|D+'
dict_alphabet['e']='è+|é+|e+|E+|3+'
dict_alphabet['f']='f+|F+'
dict_alphabet['g']='g+|G+'
dict_alphabet['h']='h+|H+'
dict_alphabet['i']='i+|I+|1+'
dict_alphabet['j']='j+|J+'
dict_alphabet['k']='k+|K+'
dict_alphabet['l']='l+|L+'
dict_alphabet['m']='m+|M+'
dict_alphabet['n']='n+|N+'
dict_alphabet['o']='o+|O+|0+'
dict_alphabet['p']='p+|P+'
dict_alphabet['q']='q+|Q+'
dict_alphabet['r']='r+|R+'
dict_alphabet['s']='s+|S+|5+'
dict_alphabet['t']='t+|T+|7+'
dict_alphabet['u']='u+|U+'
dict_alphabet['v']='v+|V+'
dict_alphabet['w']='w+|W+'
dict_alphabet['x']='x+|X+'
dict_alphabet['y']='y+|Y+'
dict_alphabet['z']='z+|Z+'
dict_alphabet[' ']='\s+'
dict_alphabet['.']='\s+'
dict_alphabet['-']='-+|\s+'
dict_alphabet[';']='\s+'
dict_alphabet['\'']='\'+|\s+'
dict_alphabet['è']='è+|é+|e+|E+'
dict_alphabet['é']='è+|é+|e+|E+'
dict_alphabet['à']='à+|a+|á+|A+|4+'
dict_alphabet['á']='à+|a+|á+|A+|4+'
dict_alphabet['ç']='ç+|c+|C+'

#All of the lexics used to generate regexes.
cage_lexic=["cage", "jail", "enclosure", "cabine", "trap", "jadi"]
birds_lexic=["bird", "macaw", "amazon", "parrot", "parakeet", "macaw", "ara", "cacato", "perruche","kakapo", "cockatoo", "lorikeet", "lori", "african grey", "conure", "parrotlet", "puteh", "hornbill", "jambul", "shama", "chicken", "ostrich", "poule", "pigeon", "swan", "paon","dove", "duck", "goose", "geese", "aves", "albatross", "aigle", "falcon", "stork", "seagull", "penguin", "eagle", "aviary", "auk", "owl", "colibri", "flamingo", "lovebird", "canary", "emu", "hen", "ibis", "kiwi", "crow", "raven", "peacock", "heron", "toucan", "turkey" ,"woodpecker", "quetzal", "puffin", "moa", "leghorn", "magpie", "junco", "kildeer", "hawk", "vulture", "egret", "grouse", "fowl", "cuckoo", "cormorant", "flicker", "wren", "chick","hyacynth", "nuquigualda", "psittacus", "psittacidae", "papagaio", "jako", "pstittacus", "guacamayo", "	psittaciforme", "guacamayito", "spix", "parot", "kakariki", "periquito", "lorito", "maracana", "peroked", "pearoid", "papagalul", "conure", "kakapu", "inseparable", "kokketiel","cocatiel", "cockatiel", "calopsitte"]
parrots_lexic=["macaw", "amazon", "parrot", "parakeet", "macaw", "ara", "cacato", "perruche","kakapo", "cockatoo", "lorikeet", "lori","lory", "african grey", "parrotlet", "hyacynth", "nuquigualda", "psittacus", "psittacidae", "papagaio", "jako", "pstittacus", "guacamayo", "	psittaciforme", "guacamayito", "spix", "parot", "kakariki", "periquito", "lorito", "maracana", "peroked", "pearoid", "papagalul", "conure", "kakapu", "inseparable", "kokketiel","cocatiel", "cockatiel", "calopsitte", "plucker", "cyclopsittini", "coryllis", "eclectus", "caïques", "pione", "papegeai", "touis", "strigops", "papegeai", "palette", "nestor", "loriquets", "micropsittes", "corella", "budgerigar", "lovebird"]
egg_lexic=["egg", "cackleberry", "eggs"]
useless_words=["and", "all", "des", "spp.", "st."]
stop_names=["Little Blue Macaw", "little blue macaw"]
too_common_words=["parrot", "cuckatoo"]
cites_lexic=["cites", "registration paper", "legal requirement", "transaction paper"]


