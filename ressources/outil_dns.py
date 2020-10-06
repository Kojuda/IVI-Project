#!/usr/bin/env python
# coding=utf-8
# authors: T. Pineau
# creation: 22.09.2020

import dns.resolver #pip install dnspython
import dns.reversename
from urllib.parse import urlparse

def url_to_hostname(url):
    if url[:7] == 'http://' or url[:8] == 'https://':
        url = urlparse(url).netloc
    return url

def getNS(hostname):
    hostname = url_to_hostname(hostname)
    try: data = dns.resolver.resolve(hostname,'NS')
    except: return None
    result = []
    for raw_data in data:
        if raw_data not in result:
            result.append(str(raw_data))
    return result

def getMX(hostname):
    hostname = url_to_hostname(hostname)
    try: data = dns.resolver.resolve(hostname, 'MX')
    except: return None
    result = []
    for raw_data in data:
        result.append({
            "server": str(raw_data.exchange),
            "preference": raw_data.preference
        })
    return result

def getIPv4(hostname):
    try:
        hostname = url_to_hostname(hostname)
        data = dns.resolver.resolve(hostname, 'A')
    except: return None
    result = []
    for raw_data in data:
        if raw_data not in result:
            result.append(str(raw_data))
    return result

def getIPv6(hostname):
    try: data = dns.resolver.resolve(hostname, 'AAAA')
    except: return None
    result = []
    for raw_data in data:
        if raw_data not in result:
            result.append(str(raw_data))
    return result

def getCNAME(hostname):
    try:
        data = dns.resolver.resolve(hostname, 'CNAME')
        return (str(data[0].target))
    except: return None


def getSOA(hostname):
    try:
        data = dns.resolver.resolve(hostname, 'SOA')
        print(data[0])
        result = {
            "server": str(data[0].mname),
            "technique": str(data[0].rname),
            "serial": str(data[0].serial),
            "refresh": str(data[0].refresh),
            "retry": str(data[0].retry),
            "expire": str(data[0].expire),
            "minimum": str(data[0].minimum)
        }
        return result
    except: return None

def getTXT(hostname):
    hostname = url_to_hostname(hostname)
    try:
        data = dns.resolver.resolve(hostname, 'TXT')
        return (str(data[0].strings))
    except: return None

def getPTR(ip):
    """ip to hostname"""
    try:
        addr = dns.reversename.from_address(ip)
        data = dns.resolver.resolve(addr, "PTR")
        return str(data[0])
    except: return None
