#!/usr/bin/env python
# coding=utf-8
# authors: D. Kohler
# creation: 13.10.20

import re, csv
from lxml import html #pip install lxml cssselect

def getURL(objet, filename):
    '''Fonction qui récupère les url, les titres de pages et la description des résultats d'une recherche Bing, puis les enregistre dans un fichier .csv'''
    csvFile = open(filename, 'w', newline='', encoding="UTF-8") #ouverture d'un fichier CSV pour écrire les résultat du parsing
    writer = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_ALL, dialect='excel')
    writer.writerow(['url', 'titre', 'description']) #écriture des en-têtes des colonnes

    for result in objet.xpath('//li[@class="b_algo"]'):
        # ~~~~~~~~~~~~ Récupération de l'URL ~~~~~~~~~~~~~ #
        url = result.xpath('.//h2/a/@href')[0]
        # ~~~~~~~ Récupération du titre de l'URL ~~~~~~~~~ #
        title = result.xpath('.//h2/a')[0].text_content()
        title = re.sub('\s+', ' ', title)
        # ~~~ Récupération de la description de l'URL ~~~~ #
        description = result.xpath('.//p')[0].text_content()
        description = re.sub('\s+', ' ', description)
        # ~~ Ecriture des résultats dans un fichier CSV ~~ #
        writer.writerow([url, title, description])

    csvFile.close() #fermeture du fichier après inscriptions des données.

# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~ Parsing des données ~~~~~~~~~~~~~ #
    objet = html.parse('./results/bing_serverCode.html')
    getURL(objet, './results/bing_parsing.csv')
