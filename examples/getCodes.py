#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import sys, os, subprocess, time
from ressources.http_requests import getHTTP # fichier http_requests.py  qui se trouve dans le dossier ressources
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

def get(url, filename_prefix='result'):
    doc = Documentation()

    # ~~~~~~~~~~~~~~~ Code serveur et réponse HTTP ~~~~~~~~~~~~~~~ #
    result = getHTTP(url)
    with open('./results/'+filename_prefix+'_serverCode.html', 'wb') as f:
        f.write(result['code_serveur'].encode('utf-8')) #écriture du résulat dans un fichier
    #documentation requests:
    doc.info['requests'] = []
    doc.info['requests'].append(result['info'])

    with open('./results/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

if __name__ == '__main__':
    url = 'https://www.bing.com/search?q=buy+fake+id'
    get(url, filename_prefix = 'bing')

    url = 'https://roidsmall.to/injections-509'
    get(url, filename_prefix = 'roidsmall')
