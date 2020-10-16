#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues
# creation: 15.10.2020

import time, json, sys, os, subprocess, re, csv
from lxml import html #pip install lxml cssselect
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

#Ouverture de adpost_parsing.csv
with open('./results/getcountries/adpost_parsing.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    for row in csv_reader:
        driver.get(str(raw[0])

#countryButton = driver.findElement(str(raw[1])).click();
#countryButton.click();

#Ecrire le résultat
#with open('./results/getcountries/test', 'wb') as f:
#    f.write(str(doc).encode('utf-8'))
