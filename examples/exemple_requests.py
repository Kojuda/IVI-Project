#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 13.09.2020

import json
import re
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.http_requests import getHTTP # fichier http_requests.py  qui se trouve dans le dossier ressources

def getURL(url, headers=None, tor=False, filename_prefix=None, path="./"):
    '''Fonction pour l'exemple qui écris dans des fichier la trace Web, le code serveur et la documentation'''


    if filename_prefix==None :
        domain=re.search("//([^/]+)/", url)
        filename_prefix=path+domain[1]
    else :
        filename_prefix="gethttp"

    # ~~~~~~~~~~~~~ Requests - script http_requests.py ~~~~~~~~~~~~~~~ #
    result = getHTTP(url, headers, tor)

    with open(filename_prefix+'_serverCode.html', 'wb') as f: #écriture du résulat dans un fichier
        f.write(result['code_serveur'].encode('utf-8'))

    # ~~~~~~~~~~~~~ Documentation - script documentation.py ~~~~~~~~~~ #
    doc = Documentation(tor=tor)
    doc.info = result['info'] #les infos venant du module http_requests seulement au moment de faire la request, il faut les ajouter

    with open(filename_prefix+'_documentation.json', 'wb') as f: #écriture du résulat dans un fichier
        f.write(str(doc).encode('utf-8'))


if __name__ == '__main__':
    headers = {
        'user-agent': 'Zafira/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'referer': None,
        'cookie': None
    }
    # getURL('http://httpbin.org/ip', path="./results/")
    # getURL('http://httpbin.org/ip', tor=True, path="./results/")    
    # getURL('http://www.fakeid.co.uk/', tor=True, path="./results/")
    # getURL('https://www.fake-id.com/', tor=True, path="./results/")
    # getURL('https://www.facebook.com/4/friends', tor=False, path="./results/")
    # getURL('https://www.google.com/recaptcha/api2/demo', tor=False, path="./results/")
    getURL('http://myhttpheader.com/', tor=False, path="./results/", headers=headers)
    print("Done")