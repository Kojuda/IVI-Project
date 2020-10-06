#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import time, pickle

from ressources.http_requests import getHTTP # fichier http_requests.py  qui se trouve dans le dossier ressources
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

def login(browser, email, password):
    '''Fonction qui permet de se connecter à Facebook avec une adresse mail et un mot de passe'''
    info = browser.get('https://www.facebook.com/') #page d'acceuil de Facebook
    print("Login sur Facebook...")

    browser.driver.find_element_by_id('email').send_keys(email)
    info['actions'].append("driver.find_element_by_id('email').send_keys(email)") #documentation

    browser.driver.find_element_by_id('pass').send_keys(password)
    info['actions'].append("driver.find_element_by_id('pass').send_keys(password)") #documentation

    browser.driver.find_element_by_xpath('//button[@name="login"]').click()
    info['actions'].append("driver.find_element_by_xpath('//button[@name=\"login\"]').click()") #documentation
    return info

def friends(browser, target):
    '''Fonction qui permet d'acceder aux amis du compte cible'''
    info = browser.get(target)
    print('Accès a tous les amis: chargement de la page entière... \n(peu prendre quelques minutes)')
    lastHeight = browser.driver.execute_script("return document.body.scrollHeight")
    n = 1 #test le scrolling, compteur pour arreter
    while True:
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5);
        newHeight = browser.driver.execute_script("return document.body.scrollHeight")
        if n >= 10:
            time.sleep(2);
            break
        if newHeight == lastHeight: n += 1
        else:
            lastHeight = newHeight
            n = 1
    info['actions'].append('driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")') #documentation
    return info

if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Configuration ~~~~~~~~~~~~~~~ #
    url = 'https://www.facebook.com/profile.php?id=100019050188166&sk=friends' #'https://www.facebook.com/4/friends'
    filename_prefix = 'facebook'
    headless = True
    cookies = False

    # ~~~~~~~~~~~~~~~ Documentation ~~~~~~~~~~~~~~~ #
    doc = Documentation()

    # ~~~~~~~~~~~~~~~ Code client et screenshot ~~~~~~~~~~~~~~~ #
    doc.info['selenium'] = []
    browser = Firefox(headless=headless) #ou Chrome(...)

    if cookies: info = browser.useCookies('https://www.facebook.com', './results/'+filename_prefix+'_cookies.pkl')
    else:
        info = login(browser, 'mon_login', 'mon_password') # Connexion au compte Facebook, modifier le login et password
        browser.saveCookies('./results/'+filename_prefix+'_cookies.pkl') #Enregistrement des cookies
    doc.info['selenium'].append(info)

    #Accès à la page voulue
    info = friends(browser, url)
    doc.info['selenium'].append(info)

    browser.clientCode('./results/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/'+filename_prefix+'_screenshot.png', width=1080)

    # ~~~~~~~~~~~~~~~ Code serveur et réponse HTTP ~~~~~~~~~~~~~~~ #
    headers = {
        'user-agent': browser.driver.execute_script("return navigator.userAgent"), #utilisé le même useragent que selenium
        'referer': 'https://www.facebook.com/', #Il faut indiquer qu'on vient d'une URL du hostname
        'cookie': ''
    }
    #Chargement des cookies
    for cookie in pickle.load(open('./results/facebook_cookies.pkl','rb')):
        headers['cookie'] += cookie['name'] + '=' + cookie['value'] + '; '

    result = getHTTP(url, headers=headers)
    with open('./results/'+filename_prefix+'_serverCode.html', 'wb') as f: #écriture du résulat dans un fichier
        f.write(result['code_serveur'].encode('utf-8'))

    #documentation requests:
    doc.info['requests'] = []
    doc.info['requests'].append(result['info'])


    # ~~~~~~~~~~~~~~~ Documentation - enregistrement ~~~~~~~~~~~~~~~ #
    with open('./results/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))
