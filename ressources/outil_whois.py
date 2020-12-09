#!/usr/bin/env python
# coding=utf-8
# authors: T. Pineau
# creation: 22.10.2020


"""
Ressource fournissant des fonctions permettant d'obtenir du protocol WHOIS. (inutilisées)
"""

import socket, re, sys
from urllib.parse import urlparse

def queryWhois(query, hostname):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, 43)) #protocole WHOIS sur port 43
        s.send(str.encode(query + "\r\n"))
        response = ''
        while True:
            d = s.recv(4096)
            response += d.decode()
            if not d:
                break
        s.close()
        return response

def ipWhois(ip):
    data = queryWhois("n "+ip, 'whois.arin.net')
    rex='(ReferralServer: whois://)([ a-zA-Z]*.[ a-zA-Z]*.[ a-zA-Z]*)'
    server = re.findall(rex, data)
    if len(server) > 0:
        data = queryWhois(ip, server[0][1])
        server = server[0][1]
    else:
        server = 'whois.arin.net'
    return (data, server)

def whois(hostname):
    """Requête WHOIS, paramètre: url, domain ou IPv4. Retourne le résultat et le serveur ayant répondu"""
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname): #si ipv4
        return ipWhois(hostname)
    else:
        if hostname[:7] in ('https:/', 'http://'): #si une url est passée en paramètre
                hostname = urlparse(hostname).netloc
        server = hostname + ".whois.iana.org"
        try:
            data = queryWhois(hostname, server)
        except:
            data = queryWhois(hostname, 'whois.iana.org')
        whoisserver_regex='whois\.[\w\-][\w\-\.]+[a-zA-Z]{1,4}'
        whoisserver = re.findall(whoisserver_regex,data)
        if len(whoisserver) > 0:
            record = queryWhois(hostname, whoisserver[0])
            server = whoisserver[0]
        return {'record':record, 'server':server}
