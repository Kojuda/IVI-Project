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
from selenium.common.exceptions import TimeoutException


def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode('./results/getCodes/codes/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/getCodes/screenshots/' + filename_prefix + '_screenshot.png', width=1080)  # on fixe la largeur de la fenêtre avec width
    #browser.serverCode('./results/getCodes/codes/'+filename_prefix+'_serverCode.html')
    #Décision de pas prendre le serveur code; car même information que client code


if __name__ == '__main__':
    cT = datetime.datetime.now()
    date_extraction = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    filename_prefix="getCodes"

    doc = Documentation()
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=True)

    # ~~~~~~~~~~~~~~~ Récupération des URL à parcourir ~~~~~~~~~~~~~ #
    for i in session.query(Urls_ads).filter_by(status=0):
        #Pour tous les urls dans la database qui ne sont pas encore extrait
        if session.query(exists().where(Ads_Codes.ad_number == i.ad_number)).scalar():
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
            saveData(browser, filename_prefix=str(i.ad_number)) #sauvgarder les codes recuperées



            with open(f'./results/getCodes/documentation/{i.ad_number}__documentation.json', 'wb') as f:
                f.write(str(doc).encode('utf-8'))
                
            entry = Ads_Codes(ad_number=i.ad_number, client_code =str(i.ad_number)+'_clientCode.html', server_code=str(i.ad_number)+'_serverCode.html')
            entry.insertCode(session)
            #i.urls_ads_update(session) #met à jour le status de l'URL
            time.sleep(random.uniform(1.5, 2.5)) #attente entre 1.5 et 2.5 sec





            # doc1 = Documentation()#Crée la documentation
            # doc1.info["selenium"] = {}  # documentation

            # doc1.info["selenium"][f"ad-{i.ad_number}"] = []  # documentation
            # doc1.info["selenium"][f"ad-{i.ad_number}"].append(info)  # documentation
              #Version all in one
            # with open(f'./results/getCodes/documentation_bis/{date_extraction}_{filename_prefix}__documentation.json', 'wb') as f:
            #     f.write(str(doc1).encode('utf-8'))
            #Version per ad