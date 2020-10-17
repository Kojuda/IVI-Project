#!/usr/bin/env python
# coding=utf-8
# author: D. Kohler, L. Rodrigues
# creation: 15.10.2020

#On importe nos deux scripts de documentation et de webdriver
import time, json, sys, os, subprocess, re, csv
from lxml import html #pip install lxml cssselect
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import Country, session
#Fonction pour sauver le code client, le screenshot et le code serveur
def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode(filename_prefix+'_clientCode.html')
    browser.screenshot(filename_prefix+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width
    browser.serverCode(filename_prefix+'_serverCode.html')


def getURL(objet, session, original_url):
    '''Fonction qui récupère les url, les titres de pages et la description des résultats d'une recherche Bing, puis les enregistre dans un fichier .csv'''
    
    for countries in objet.xpath('//div[@class="countries"]'):
        for country in countries.xpath('.//div'):
            # ~~~~~~~~~~~~ Récupération de l'URL ~~~~~~~~~~~~~ #
            url = original_url + country.xpath('.//a/@href')[0]
            # ~~~~~~~~~~~~ Récupération du nom associé ~~~~~~~~~~~~~ #
            name = country.xpath('.//a/text()')[0]
            # ~~ Ecriture des résultats dans un fichier CSV ~~ #
            # Country(name=name, url=url).insertCountry(session)


# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Ouverture du port de Tor (pour MAC OS ou Windows, on aura en arrière fond le port Tor, plus besoin d'avoir le navigateur Tor ouvert) ~~~~~~~~~~~~~~~ #
    if sys.platform == 'win32':
        tor_process = subprocess.Popen(os.getcwd() + r'\webdrivers\win_Tor\tor.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if sys.platform == 'darwin':
        tor_process = subprocess.Popen(os.getcwd() + r'/webdrivers/osx_Tor/tor.real', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=True) #ou Chrome(...)

    doc = Documentation(driver=browser.driver)
    # Vous pouvez compléter l'objet doc avec les urls parcourues et les manipulations effectuées!

    url = 'https://www.adpost.com'
    browser.driver.get(url)
    saveData(browser, filename_prefix='./results/getcountries/adpost')


    # ~~~~~~~~~~~~ Parsing des données ~~~~~~~~~~~~~ #
    objet = html.parse('./results/getcountries/adpost_serverCode.html')
    getURL(objet, session, url) #original_url = url
    doc.addlog("getURL(objet, session, url)")
    #Enregistrement de la documentation dans un fichier .json
    with open('./results/getcountries/documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

    # ~~~~~~~~~~~~~~~ Fermeture du port de Tor ~~~~~~~~~~~~~~~ #
    #tor_process.kill()
