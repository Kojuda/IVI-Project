#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

from ressources.http_requests import getHTTP #fichier http_requests.py  qui se trouve dans le dossier ressources
from ressources.db import session, insertURL #fichier db.py  qui se trouve dans le dossier ressources
import lxml.html


#Page anibis qui nous permet de récupérer les URL des annonces
base_url = 'https://www.anibis.ch'
url = "https://www.anibis.ch/fr/c/bijouterie-horlogerie-pierres-precieuses/diamant-diamant-brut"
result = getHTTP(url)
with open('./results/sources_url/anibis.html', 'wb') as f: f.write(result['code_serveur'].encode('utf-8'))

#Parsing pour récupérer les URL pour l'étape de collecte
html = lxml.html.parse('./results/sources_url/anibis.html').getroot()
liste = html.xpath('//article/a/@href') #les liens des annonces
for i in liste: insertURL(session, base_url+i)
