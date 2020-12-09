#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 13.09.2020

"""
Ressource permettant d'utiliser des requêtes HTTP via le module requests.
"""


import datetime, json
import requests #pip install requests requests[socks] pysocks

def getHTTP(url, headers=None, tor=False):
    '''Fonction qui execute une requête avec la librarie Python "requests"'''
    if headers == None: #headers par défaut.
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'referer': None,
            'cookie': None
        }
    if tor:
        proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'} #port 9050 si Tor est configuré comme un service
    else: 
        proxies = {"http": None, "https": None}
    dateRequest = datetime.datetime.now().astimezone().isoformat() #date de la requête avec fuseau local
    response = requests.get(url, headers=headers, proxies=proxies)

    documentation = {
            'request': {
            'date': dateRequest,
            'url': url,
            'headers': dict(response.request.headers),
            'proxies': proxies,
            },
            'response': {
                'url': response.url, #peut être différente de request_url s'il y a eu une redirection
                'status': response.status_code,
                'headers': dict(response.headers),
                'elapsed': str(response.elapsed)
            }
        }
    code = response.text
    return {'info': documentation, 'code_serveur': code}
