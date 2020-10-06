#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import sys, os, subprocess, time
from ressources.http_requests import getHTTP # fichier http_requests.py  qui se trouve dans le dossier ressources
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Configuration ~~~~~~~~~~~~~~~ #
    url = 'https://www.fakeid.co.uk/'
    filename_prefix = 'fakeidcouk'
    tor = False
    headless = True

    # ~~~~~~~~~~~~~~~ Ouverture du port de Tor, si besoin ~~~~~~~~~~~~~~~ #
    if tor:
        if sys.platform == 'win32':
            tor_process = subprocess.Popen(os.getcwd() + r'\webdrivers\win_Tor\tor.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if sys.platform == 'darwin':
            tor_process = subprocess.Popen(os.getcwd() + r'/webdrivers/osx_Tor/tor.real', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ~~~~~~~~~~~~~~~ Documentation ~~~~~~~~~~~~~~~ #
    doc = Documentation(tor=tor)

    # ~~~~~~~~~~~~~~~ Code client et screenshot ~~~~~~~~~~~~~~~ #
    browser = Firefox(headless=headless, tor=tor) #ou Chrome(...)
    info = browser.get(url)
    browser.clientCode('./results/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/'+filename_prefix+'_screenshot.png', width=1080)
    #documentation selenium:
    doc.info['selenium'] = []
    doc.info['selenium'].append(info)

    # ~~~~~~~~~~~~~~~ Code serveur et réponse HTTP ~~~~~~~~~~~~~~~ #
    result = getHTTP(url, tor=tor)
    with open('./results/'+filename_prefix+'_serverCode.html', 'wb') as f:
        f.write(result['code_serveur'].encode('utf-8')) #écriture du résulat dans un fichier
    #documentation requests:
    doc.info['requests'] = []
    doc.info['requests'].append(result['info'])

    # ~~~~~~~~~~~~~~~ Documentation - enregistrement ~~~~~~~~~~~~~~~ #
    with open('./results/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

    # ~~~~~~~~~~~~~~~ Fermeture du port de Tor, si besoin ~~~~~~~~~~~~~~~ #
    if tor: tor_process.kill()
