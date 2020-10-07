#!/usr/bin/env python
# coding=utf-8
# authors: T. Pineau
# creation: 06.10.2020

import re, csv
from lxml import html #pip install lxml cssselect

def getProducts(objet, filename):
    csvFile = open(filename, 'w', newline='', encoding="UTF-8") #ouverture d'un fichier CSV pour écrire les résultat du parsing
    writer = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_ALL, dialect='excel')
    writer.writerow(['nom', 'prix', 'manufactureur', 'drugClass', 'substances', 'concentration', 'noms_communs', 'package']) #écriture des en-têtes des colonnes

    for product in objet.xpath('//ul[@class="product-list"]/li'):
        try: name = product.xpath('.//h4/a')[0].text.strip()
        except: continue
        price = product.xpath('.//ins')[0].text.strip()
        description = product.xpath('.//div/div')
        if description  == []: description = '' #pas de description
        else: description = description[0].text_content()

        ####Parsing de la description avec REGEX####

        drugClass = re.findall('Drug Class:(.*)', description)
        if drugClass == []: drugClass=''
        else: drugClass = drugClass[0].strip()

        commonNames = re.findall('Common Name\(s\):(.*)', description)
        if commonNames == []: commonNames=''
        else: commonNames = commonNames[0].strip()

        manufacturer = re.findall('Manufacturer:(.*)', description)
        if manufacturer == []: manufacturer=''
        else: manufacturer = manufacturer[-1].strip()
        if 'Common Name' in manufacturer: manufacturer = manufacturer.split(' Common Name')[0] #certains produits sont mal formaté par rapport au reste

        substance = re.findall('Substance[s]?:(.*)', description)
        if substance == []: substance=''
        else: substance = substance[0].strip()

        concentration = re.findall('Concentration:(.*)', description)
        if concentration == []: concentration=''
        else: concentration = concentration[0].strip()

        package = re.findall('(?:Package|Presentation):(.*)', description)
        if package == []: package=''
        else: package = package[0].strip()

        ####Ecriture des résultats dans un fichier CSV####
        writer.writerow([name, price, manufacturer, drugClass, substance, concentration, commonNames, package])

    csvFile.close() #fermeture du fichier après inscriptions des amis.

# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~ Parsing des données ~~~~~~~~~~~~~ #
    objet = html.parse('./results/roidsmall_serverCode.html')
    getProducts(objet, './results/roidsmall_parsing.csv')
