#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020

import os, platform, json
from pipreqs import pipreqs # pip install pipreqs
import requests # pip install requests requests[socks] pysocks
import datetime

class Documentation():
    def __init__(self, tor=False, info={}, driver=False, log = {}):
        self.path = os.path.dirname(os.path.realpath(__file__)) #le chemin du dossier où est exécuté le fichier
        self.info = info
        self.tor = tor
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
            if self.tor: proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            else: proxies = {}
            try: self.ip = requests.get('http://httpbin.org/ip', proxies=proxies).json()['origin'] #utilisation du service ipinfo.io
            except: print('Documentation - erreur à retrouvé l\'adresse IP publique.')

    def toJSON(self):
        """Retourne l'objet dans le format JSON"""
        return {
            'ip': self.ip,
            'tor': self.tor,
            'programm': self.programm,
            'system': self.system,
            'info': self.info,
            'log' : self.log
        }
    def addlog(self, string="") :
        cT=datetime.datetime.now() #cT=current time
        time=f"{str(cT.year)}.{str(cT.month)}.{str(cT.day)} {str(cT.hour)}:{str(cT.minute)}:{str(cT.second)}.{str(cT.microsecond)}"
        self.log[time]=string 
        #time="{}:{}:{}.{}\t {}.{}.{}".format(str(cT.hour), str(cT.minute), str(cT.second), str(cT.microsecond), str(cT.day), str(cT.month), str(cT.year))

    def __str__(self):
        """Pour afficher l'objet avec la fonction print(objet)"""
        return json.dumps(self.toJSON(), indent=4)
