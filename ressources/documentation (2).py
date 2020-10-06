#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 13.09.2020

import os, platform, json
from pipreqs import pipreqs # pip install pipreqs
import requests # pip install requests requests[socks] pysocks

class Documentation():
    def __init__(self, tor=False, info={}):
        self.path = os.path.dirname(os.path.realpath(__file__)) #le chemin du dossier où est exécuté le fichier
        self.info = info
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
        self.ip = {}
        if tor: proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'} #port 9050 si Tor est configuré comme un service
        else: proxies = {"http": None, "https": None}
        try: self.ip = requests.get('http://httpbin.org/ip', proxies=proxies).json()['origin'] #utilisation du service ipinfo.io
        except: print('Documentation - erreur à retrouver l\'adresse IP publique.')

    def toJSON(self):
        """Retourne l'objet dans le format JSON"""
        return {
            'ip': self.ip,
            'programm': self.programm,
            'system': self.system,
            'info': self.info
        }

    def __str__(self):
        """Pour afficher l'objet avec la fonction print(objet)"""
        return json.dumps(self.toJSON(), indent=4)
