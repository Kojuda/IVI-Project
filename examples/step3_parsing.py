#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import os, json, re, datetime, csv
import lxml.html #pip install lxml

def parse(filename):
    objet = lxml.html.parse(filename).getroot()
    stateScript = objet.xpath("//script[@id='state']")
    data = re.search(r'window.__INITIAL_STATE__\s*=\s*(.*)\s*', stateScript[0].text, flags=re.DOTALL)[1]
    data = re.sub('\s+',' ', data)
    data = json.loads(data)['detail']
    result = {
        'annonce_id': valeur(data, 'annonce_id'),
        'auteur_id': valeur(data, 'auteur_id'),
        'date': valeur(data, 'date'),
        'categorie': valeur(data, 'categories'),
        'titre': valeur(data, 'titre'),
        'description': valeur(data, 'description'),
        'adresse': valeur(data, 'adresse'),
        'ville': valeur(data, 'ville'),
        'prix': valeur(data, 'prix'),
        'phone': valeur(data, 'phone'),
        'website': valeur(data, 'url')
    }
    return result

def valeur(data, nom):
    result = ''
    if nom == 'annonce_id':
        if 'id' in data.keys(): result = 'anibis_' + str(data['id'])
    if nom == 'auteur_id':
        if 'seller' in data.keys() and 'id' in data['seller'].keys(): result = 'anibis_' + str(data['seller']['id'])
    elif nom == 'date':
        if 'formattedModified' in data.keys(): result = datetime.datetime.strptime(data['formattedModified'], '%d.%m.%Y')
    elif nom == 'titre':
        if 'title' in data.keys(): result = data['title']
    elif nom == 'description':
        if 'description' in data.keys():
            objet = lxml.html.document_fromstring('<html>'+data['description']+'</html>')
            result = objet.text_content()
    elif nom == 'categories':
        if 'categories' in data.keys():
            if len(data['categories']) > 1: result += data['categories'][1]['name']
            if len(data['categories']) > 2:
                for cat in data['categories'][2:]:
                    result += ' > ' + cat['name']
    elif nom == 'adresse':
        if 'location' in data.keys():
            if 'street' in data['location'].keys(): result += data['location']['street']
            if 'zipCity' in data['location'].keys(): result += ('\n' if result != '' else '') + data['location']['zipCity']
    elif nom == 'ville':
        if 'location' in data.keys():
            if 'zipCity' in data['location'].keys(): return data['location']['zipCity']
    elif nom == 'prix':
        if 'formattedPrice' in data.keys(): result = data['formattedPrice']
    elif nom == 'phone':
        if 'contact' in data.keys() and 'phone' in data['contact'].keys(): result = re.sub('\s', '', data['contact']['phone'])
    elif nom == 'url':
        if 'website' in data.keys():
            url_parse = urlparse(data['website']['url'])
            result = url_parse.netloc+url_parse.path
    result = re.sub("\s+", " ", str(result)).strip() #supprime les multiples espaces et les retours à la ligne
    return result

if __name__ == '__main__':
    with open('./results/data.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL, dialect='excel')
        headers = ['annonce_id', 'auteur_id', 'date', 'categorie', 'titre', 'description', 'adresse', 'ville', 'prix', 'phone', 'website']
        writer.writerow(headers)

        for filename in os.listdir('./results/html'): #Parsing des fichier contenus dans le dossier results/html
            if filename.endswith('clientCode.html'): #on parse que les codes clients
                obj = parse('./results/html/'+filename)
                writer.writerow([obj[key] for key in headers]) #transforme le dict en list à l'aide des clefs listées dans headers
