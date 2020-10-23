#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# modified & adapted: Luisa Rodrigues & Jasmin Wyss
# creation: 06.10.2020
# But extraire tous les urls
import time, json, random
from sqlalchemy.sql import exists
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import * #fichier db.py  qui se trouve dans le dossier ressources


def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode('./results/getCodes/codes/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/getCodes/screenshots/' + filename_prefix + '_screenshot.png', width=1080)  # on fixe la largeur de la fenêtre avec width
    browser.serverCode('./results/getCodes/codes/'+filename_prefix+'_serverCode.html')


if __name__ == '__main__':

    doc = Documentation()#Crée la documentation
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=False)

    # ~~~~~~~~~~~~~~~ Récupération des URL à parcourir ~~~~~~~~~~~~~ #
    for i in session.query(Urls_ads).filter_by(status=0):
        #Pour tous les urls dans la database qui ne sont pas encore extrait
        if session.query(exists().where(Ads_Codes.ad_number == i.ad_number)).scalar():
            pass
        else:
            doc.info['selenium'] = []  # documentation
            info = browser.get(i.url)
            doc.info['selenium'].append(info)  # documentation
            saveData(browser, filename_prefix=str(i.ad_number)) #sauvgarder les codes recuperées
            with open('./results/getCodes/documentation/'+str(i.ad_number)+'_documentation.json', 'wb') as f:
                f.write(str(doc).encode('utf-8'))
            entry = Ads_Codes(ad_number=i.ad_number, client_code =str(i.ad_number)+'_clientCode.html', server_code=str(i.ad_number)+'_serverCode.html')
            entry.insertCode(session)
            Urls_ads.urls_ads_update(session, i) #met à jour le status de l'URL
            time.sleep(random.uniform(1.5, 2.5)) #attente entre 1.5 et 2.5 sec
