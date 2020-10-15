#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020

#On importe nos deux scripts de documentation et de webdriver
import time, json, sys, os, subprocess
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

#Fonction pour sauver le code client, le screenshot et le code serveur
def saveData(browser, filename_prefix='selenium'):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode(filename_prefix+'_clientCode.html')
    browser.screenshot(filename_prefix+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width
    browser.serverCode(filename_prefix+'_serverCode.html')


# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Ouverture du port de Tor (pour MAC OS ou Windows, on aura en arrière fond le port Tor, plus besoin d'avoir le navigateur Tor ouvert) ~~~~~~~~~~~~~~~ #
    if sys.platform == 'win32':
        tor_process = subprocess.Popen(os.getcwd() + r'\webdrivers\win_Tor\tor.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if sys.platform == 'darwin':
        tor_process = subprocess.Popen(os.getcwd() + r'/webdrivers/osx_Tor/tor.real', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    browser = Chrome(tor=False, headless=False) #ou Chrome(...)

    doc = Documentation(driver=browser.driver)
    # Vous pouvez compléter l'objet doc avec les urls parcourues et les manipulations effectuées!

    url1 = 'https://www.adpost.com/'
    browser.driver.get(url1)
    saveData(browser, filename_prefix='./results/adpost')

    # url2 = 'https://www.unil.ch'
    # browser.driver.get(url2)
    # saveData(browser, filename_prefix='./results/unil')


    #Enregistrement de la documentation dans un fichier .json
    with open('./results/documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

    # ~~~~~~~~~~~~~~~ Fermeture du port de Tor ~~~~~~~~~~~~~~~ #
    tor_process.kill()
