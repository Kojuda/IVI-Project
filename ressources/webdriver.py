#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020
# modifications: Fonctions mis à disposition par Q.Rossy
# modification: 19.10.2020
import sys, os, datetime, pickle
from selenium import webdriver #pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from outil_dns import url_to_hostname, getIPv4
import time

class Browser:
    def get(self, url):
        """Demande l'accès à l'URL et retourne les infos pour la documentation"""
        dateRequest = datetime.datetime.now().astimezone().isoformat() #mets le timestamp de la demande
        headers = {
            'user-agent': self.driver.execute_script("return navigator.userAgent"),
            'referer': self.driver.current_url,
            'cookie': self.driver.get_cookies()
        }
        self.driver.get(url)
        documentation = {
                'request': {
                    'date': dateRequest,
                    'url': url,
                    'headers': headers
                },
                'response': {
                    'url': self.driver.current_url, #peut être différente de request_url s'il y a eu une redirection
                    #PROJET ADD
                    'ip_server' : getIPv4(self.driver.current_url)
                },
                'actions': []
            }
        return documentation

    def useCookies(self, url_start, pkl_filename):
        info = self.get(url_start) #url_start l'url d'accueil on on va "injecter" les cookies
        self.driver.delete_all_cookies()
        for cookie in pickle.load(open(pkl_filename,'rb')): self.driver.add_cookie(cookie)
        info['actions'].append("driver.delete_all_cookies()") #documentation
        info['actions'].append("for cookie in pickle.load(open(pkl_file,'rb')): driver.add_cookie(cookie)") #documentation
        return info

    def saveCookies(self, pkl_filename):
        pickle.dump(self.driver.get_cookies(), open(pkl_filename,'wb'))

    def clientCode(self, outputPath, encoding='utf-8'):
        """Enregistre le code client"""
        client_code = self.driver.page_source #self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        with open(outputPath, 'wb') as f:
            f.write(client_code.encode(encoding))

    def screenshot(self, outputPath, width=None):
        """La capture est complète uniquement en mode headless, on peut fixer la largeur avec width"""
        if width==None: width = self.driver.execute_script('return document.documentElement.scrollWidth') #largeur maximale
        heightMax = self.driver.execute_script('return document.documentElement.scrollHeight') #hauteur maximale
        self.driver.set_window_size(width, heightMax)
        self.driver.save_screenshot(outputPath)

    def serverCode(self, outputPath, encoding='utf-8'):
        """Enregistre le code serveur, à faire en dernier car change la page"""
        url = self.driver.current_url
        self.driver.get('view-source:'+url)
        server_code = self.driver.find_element_by_xpath("//*").text
        with open(outputPath, 'wb') as f:
            f.write(server_code.encode(encoding))

    def wait(self, time=30) :
        WebDriverWait(self.driver, timeout=time).until(lambda x : x==1) #Condition always true

    def __del__(self):
        try: self.driver.quit()
        except: None

class Chrome(Browser):
    def __init__(self, tor=False, headless=False, useragent=False):
        #Chemin vers le webdriver téléchargé - A changer si nécessaire
        if sys.platform == 'win32': driverFile = os.getcwd() + r'\webdrivers\chromedriver.exe' #Windows
        if sys.platform == 'darwin': driverFile = os.getcwd() + r'/webdrivers/chromedriver' #OSX

        #Configuration du webdriver
        options = webdriver.chrome.options.Options()
        if headless: options.add_argument('--headless') #masque la fenêtre
        if useragent: options.add_argument('--user-agent='+useragent)
        options.add_argument('log-level=3') #cache les messages d'info du navigateur
        if tor: options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

        #Instanciation du webdriver
        self.driver = webdriver.Chrome(executable_path=driverFile, options=options)

class Firefox(Browser):
    def __init__(self, tor=False, headless=False, useragent=False):
        #Chemin vers le webdriver téléchargé - A changer si nécessaire
        if sys.platform == 'win32': driverFile = os.getcwd() + r'\webdrivers\geckodriver.exe' #Windows
        if sys.platform == 'darwin': driverFile = os.getcwd() + r'/webdrivers/geckodriver' #OSX

        #Configuration du webdriver
        options = webdriver.firefox.options.Options()
        if headless: options.set_headless(headless=True) #masque la fenêtre, False pour l'afficher
        options.set_preference("dom.push.enabled", False) #bloque les popup de notifications
        profile = webdriver.FirefoxProfile()
        if useragent: profile.set_preference("general.useragent.override", useragent)
        if tor:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.socks", "127.0.0.1")
            profile.set_preference("network.proxy.socks_port", 9050)
            profile.set_preference("network.proxy.socks_version", 5)
            profile.set_preference("network.proxy.socks_remote_dns", True)

        #Instanciation du webdriver
        self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=driverFile, options=options)

def switchJavascriptChrome(driver):
    #Affichage de la page des paramètres de Chrome
    driver.get('chrome://settings/content/javascript?search=javascript')
    time.sleep(1)
#Le bouton radio est dans un zone cachée de l’HTML (ShadowRoot), il faut lancer un script
    toggle = driver.execute_script('return document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-privacy-page").shadowRoot.querySelector("#pages > settings-subpage.iron-selected > category-default-setting").shadowRoot.querySelector("#toggle").shadowRoot.querySelector("#control")')
    time.sleep(1)
    try:
        toggle.click()
        time.sleep(0.2)
        driver.refresh()
    except: #En cas de problème on recommence
        switchJavascriptChrome(driver)


def switchJavascriptFirefox(driver):
#Affichage de la page des paramètres de Chrome
    driver.get('about:config')
#Clic du bouton de Warning
    button = driver.find_element_by_xpath('//button[contains(@id, "warningButton")]')
    button.click()
#Saisie de la recherche du parametre
    search = driver.find_element_by_xpath('//input[contains(@id,"about-config-search")]')
    search.send_keys("javascript.enabled")
    time.sleep(1)
#Clic pour désactiver
    span = driver.find_element_by_xpath('//html/body/table/tr[1]/td[1]/span')
    actionChains = webdriver.common.action_chains.ActionChains(driver)
    actionChains.double_click(span).perform()
    time.sleep(0.2)
    driver.back()
    driver.refresh()

