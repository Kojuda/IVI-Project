#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import time, pickle
from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Configuration ~~~~~~~~~~~~~~~ #
    url = 'https://www.google.com/recaptcha/api2/demo'
    filename_prefix = 'recaptcha'
    headless = False


    # ~~~~~~~~~~~~~~~ Documentation ~~~~~~~~~~~~~~~ #
    doc = Documentation()

    # ~~~~~~~~~~~~~~~ Code client et screenshot ~~~~~~~~~~~~~~~ #
    browser = Firefox(headless=headless) #ou Chrome(...)
    info = browser.get(url)

    wait = WebDriverWait(browser.driver, 120) #temps d’att. max. en secondes
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="recaptcha-success"]'))) #attente de l'élément pour reprendre
    info['url_final'] = browser.driver.current_url #au cas où on changerai de page pendant le wait.

    browser.clientCode('./results/'+filename_prefix+'_clientCode.html')
    browser.screenshot('./results/'+filename_prefix+'_screenshot.png', width=1080)

    #documentation selenium:
    doc.info['selenium'] = []
    info['actions'].append('WebDriverWait(browser.driver, 120).until(EC.presence_of_element_located((By.XPATH, \'//div[@class="recaptcha-success"]\')))')
    info['actions'].append('Résolution du recaptcha manuellement et validation')
    doc.info['selenium'].append(info)

    #Enregistrement des cookies
    cookies = browser.driver.get_cookies()
    pickle.dump(cookies , open('./results/'+filename_prefix+'_cookies.pkl','wb'))


    # ~~~~~~~~~~~~~~~ Documentation - enregistrement ~~~~~~~~~~~~~~~ #
    with open('./results/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))
