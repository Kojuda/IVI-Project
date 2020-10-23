#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# modified & adapted: Luisa Rogrigues & Jasmin Wyss
# creation: 06.10.2020
# But extraire tous les urls
import time, json, random
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import * #fichier db.py  qui se trouve dans le dossier ressources

def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode('./results/getCodes/codes'+filename_prefix+'_clientCode.html')
    browser.serverCode('./results/getCodes/codes'+filename_prefix+'_serverCode.html')
    browser.screenshot('./results/getCodes/screenshots/'+filename_prefix+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width

if __name__ == '__main__':
    doc = Documentation()#Crée la documentation
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=False)

    # ~~~~~~~~~~~~~~~ Récupération des URL à parcourir ~~~~~~~~~~~~~ #
    # TODO:  Solve for this SQL expression, column, or mapped entity expected - got '<class 'ressources.db.Url'>'
    for i in session.query(Url_ads).filter_by(status=0):
        #Pour tous les urls dans la database qui ne sont pas encore extrait
        doc.info['selenium'] = []
        info = browser.get(i.url)
        doc.info['selenium'].append(info)
        saveData(browser, filename_prefix=str(i.id))



        with open('./results/documentation/'+str(i.id)+'_documentation.json', 'wb') as f:
            f.write(str(doc).encode('utf-8'))
        updateURL(session, i) #met à jour le status de l'URL
        time.sleep(random.uniform(1.5, 2.5)) #attente entre 1.5 et 2.5 sec
