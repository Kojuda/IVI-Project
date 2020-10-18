#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 06.10.2020

import sys, os, datetime, pickle
from selenium import webdriver #pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Browser:
    def get(self, url):
        """Demande l'accès à l'URL et retourne les infos pour la documentation"""
        dateRequest = datetime.datetime.now().astimezone().isoformat()
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
