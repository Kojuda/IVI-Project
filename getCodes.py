#!/usr/bin/env python
# coding=utf-8

"""
Ce script parcourt les urls des annonces récoltées dans la base de données dans la table "urls_ades"
pour extraire les codes clients des annonces ainsi que le screenshot de ces dernières. Les noms des codes
extraits sont stockés dans la table "ads_codes" et les données comprenant les codes clients et les screenshots
sont stockées dans le sous-répertoire de "results" concernant ce script.
"""


import time, json, random, os
from sqlalchemy.sql import exists
from ressources.webdriver import Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import * #fichier db.py  qui se trouve dans le dossier ressources
from selenium.common.exceptions import TimeoutException
from ressources.project_utils import get_abr_country


def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode('./results/getCodes/codes/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/getCodes/screenshots/' + filename_prefix + '_screenshot.png', width=1080)  # on fixe la largeur de la fenêtre avec width
    #Décision de pas prendre le serveur code; car même information que client code


if __name__ == '__main__':
    cT = datetime.datetime.now()
    date_extraction = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    filename_prefix="getCodes"

    doc = Documentation()

    #Create the directory
    os.makedirs(os.path.dirname("./results/getCodes/documentation/"), exist_ok=True)
    os.makedirs(os.path.dirname("./results/getCodes/codes/"), exist_ok=True)
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=True)

    # ~~~~~~~~~~~~~~~ Récupération des URL à parcourir ~~~~~~~~~~~~~ #
    for i in session.query(Urls_ads).filter_by(status=0):
        #Pour tous les urls dans la database qui ne sont pas encore extrait
        if session.query(exists().where(Ads_Codes.ad_id == i.ad_id)).scalar():
            pass
        else:
            pass_test=0
            while not pass_test :
                try :
                    info = browser.get(i.url)
                    pass_test=1
                except TimeoutException as e:
                    doc.adderrorlog(f"{e}")
                    pass
                except :
                    doc.adderrorlog(f"Unknown error")
                    pass


            doc.info["selenium"] = []  # documentation
            doc.info["selenium"].append(info)  # documentation
            abr_country=get_abr_country(i.url)
            saveData(browser, filename_prefix=f"{i.ad_number}_{abr_country}") #sauvgarder les codes recuperées



            with open(f'./results/getCodes/documentation/{i.ad_number}_{abr_country}__documentation.json', 'wb') as f:
                f.write(str(doc).encode('utf-8'))
            entry = Ads_Codes(ad_id=f"{i.ad_number}_{abr_country}" ,ad_number=i.ad_number, client_code =f"{i.ad_number}_{abr_country}_clientCode.html")
            entry.insertCode(session)
            i.urls_ads_update(session) #met à jour le status de l'URL
            time.sleep(random.uniform(0.1, 1.5)) #attente entre 1.5 et 2.5 sec
