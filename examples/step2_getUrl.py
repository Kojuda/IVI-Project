#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import time, json, random
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import session, updateURL, Url #fichier db.py  qui se trouve dans le dossier ressources

def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode('./results/html/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/screenshots/'+filename_prefix+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width

if __name__ == '__main__':
    doc = Documentation()
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Chrome(headless=True) #ou Chrome(...)

    # ~~~~~~~~~~~~~~~ Récupération des URL à parcourir ~~~~~~~~~~~~~ #
    for i in session.query(Url).filter_by(status=0):
        doc.info['selenium'] = []
        info = browser.get(i.url)
        doc.info['selenium'].append(info)
        saveData(browser, filename_prefix=str(i.id))
        with open('./results/documentation/'+str(i.id)+'_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
        updateURL(session, i) #met à jour le status de l'URL
        time.sleep(random.uniform(0.1, 0.2)) #attente entre 1.5 et 2.5 sec
