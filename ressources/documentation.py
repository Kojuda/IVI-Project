#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020

import os, platform, json, datetime
from pipreqs import pipreqs # pip install pipreqs
import requests # pip install requests requests[socks] pysocks

class Documentation():
    def __init__(self, tor=False, info={}, driver=False, log={}):
        self.path = os.path.dirname(os.path.realpath(__file__)) #le chemin du dossier où est exécuté le fichier
        self.info = info
        self.log = log
        self.programm = {
            'software': "Python",
            'software_version': platform.python_version(),
            'modules': pipreqs.get_imports_info(pipreqs.get_all_imports(self.path, encoding='utf-8'))
        }
        self.system = {
            'os_name': platform.system(),
            'computer_name': platform.node(),
            'os_release': platform.release(),
            'os_version': platform.version(),
            'processor': platform.processor()
        }
        self.ip = ''
        if driver:
            try:
                driver.get('http://httpbin.org/ip')
                content = driver.find_element_by_xpath("//body").text
                self.ip = json.loads(content)['origin']
            except: print('Documentation - erreur à retrouvé l\'adresse IP publique.')
        else:
            if tor: proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'} #port 9050 si Tor est configuré comme un service
            else: proxies = {"http": None, "https": None}
            try: self.ip = requests.get('http://httpbin.org/ip', proxies=proxies).json()['origin'] #utilisation du service ipinfo.io
            except: print('Documentation - erreur à retrouvé l\'adresse IP publique.')


    def toJSON(self):
        """Retourne l'objet dans le format JSON"""
        return {
            'ip': self.ip,
            'programm': self.programm,
            'system': self.system,
            'info': self.info
        }
    #Personal adding : add a action's log to a list of strings
    def addLog(self, string="") :
        pass
        #TODO : faire en sorte d'utiliser en compteur (singleton) pour ajouter une entrée dans le dictionnaire log avec le timestamp par le module datetime
#          currentTime=datetime.datetime.now()
#                 time="{}:{}:{}.{}\t {}.{}.{}".format(str(currentTime.hour), str(currentTime.minute), str(currentTime.second), str(currentTime.microsecond), str(currentTime.day), str(currentTime.month), str(currentTime.year))
    def __str__(self):
        """Pour afficher l'objet avec la fonction print(objet)"""
        return json.dumps(self.toJSON(), indent=4)
