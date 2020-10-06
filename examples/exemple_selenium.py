#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020

import time, json, sys, os, subprocess
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources


a=os.path.dirname(r"{}".format(str(os.path.abspath(__file__))))
os.chdir(a)
def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode(filename_prefix+'_clientCode.html')
    browser.screenshot(filename_prefix+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width
    browser.serverCode(filename_prefix+'_serverCode.html')


# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Ouverture du port de Tor ~~~~~~~~~~~~~~~ #
    if sys.platform == 'win32':
        tor_process = subprocess.Popen(os.getcwd() + r'\webdrivers\win_Tor\tor.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if sys.platform == 'darwin':
        tor_process = subprocess.Popen(os.getcwd() + r'/webdrivers/osx_Tor/tor.real', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Firefox(tor=False, headless=False) #ou Chrome(...)

    doc = Documentation(driver=browser.driver)
    # Vous pouvez compléter l'objet doc avec les urls parcourues et les manipulations effectuées!

    # url1 = 'https://facebookcorewwwi.onion'
    # browser.driver.get(url1)
    # saveData(browser, filename_prefix='./results/fb-onion')

    # url2 = 'https://www.unil.ch'
    # browser.driver.get(url2)
    # saveData(browser, filename_prefix='./results/unil')

    # url4 = 'http://www.fakeid.co.uk/'
    # browser.driver.get(url4)
    # saveData(browser, filename_prefix='./results/fakeid')

    # url5 = 'https://www.fake-id.com/'
    # browser.driver.get(url5)
    # saveData(browser, filename_prefix='./results/fake-id')

    # url6 = 'https://www.facebook.com/4/friends'
    # browser.driver.get(url6)
    # browser.loginFace(user="Ana.Grames@protonmail.com", pwd="001355s071a") #Ana.Grames@protonmail.com / grames.ana@gmail.com
    # browser.wait(time=10)
    # #browser.driver.get(url6)
    # saveData(browser, filename_prefix='./results/facebook_login')

    url7 = 'https://www.google.com/recaptcha/api2/demo'
    browser.driver.get(url7)
    browser.wait(time=60)
    saveData(browser, filename_prefix='./results/google')


    #Enregistrement de la documentation dans un fichier .json
    with open('./results/documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))


    # ~~~~~~~~~~~~~~~ Shut down the webdriver ~~~~~~~~~~~~~~~ #

    browser.driver.quit()
    # ~~~~~~~~~~~~~~~ Fermeture du port de Tor ~~~~~~~~~~~~~~~ #
    tor_process.kill()
