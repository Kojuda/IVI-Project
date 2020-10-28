#!/usr/bin/env python
# coding=utf-8
# author: L.Lopez
# creation: 25.10.2020
# But: parser les pages web

import time, json, random
from sqlalchemy.sql import exists
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import * #fichier db.py  qui se trouve dans le dossier ressources
from selenium import webdriver
import re


def main():


    driver= webdriver.Firefox(executable_path=r"webdrivers/geckodriver")
    urls = open("results\getArticles\2020-10-21_0-59_urlArticles_documentation.json", “r”) # c'est un exemple en attendant le résultat getCodes
    for url in urls:
        driver.get(url)

        rows = driver.find_elements_by_class_name('row')

        for row in rows:
            balise_b = driver.find_element_by_xpath("//b")
            test = balise_b.find_element_by_xpath("./..").find_element_by_xpath("//div").text
            test = test.strip()
            test = test.replace('\n', '')
            category = re.search("Category\:(.*).+?(?=Ad+\s+Number)", test).group(1) ## https://stackoverflow.com/questions/7124778/how-to-match-anything-up-until-this-sequence-of-characters-in-a-regular-expres

            list = ['Reply+\s+to+\s+Ad','Category', 'Ad+\s+Number', 'Description', 'Breed','Age','Sex','Primilary+\s+Color','Secondary+\s+Color','Advertiser','Price','Payment+\s+Forms','Estimated+\s+Shipping','Posted+\s+By|Contact+\s+Information','Name','Zip+\s+Code|Postal+\s+Code|Post+\s+Code ','City','State+\s+>+\s+District|State+\s+>+\s+City|State+\s+>+\s+County|Province+\s+>+\s+County|Province+\s+>+\s+City|Region+\s+>+\s+County|Region|County|State+\s+>+\s+Metro','Country','Email'] # Reply to AD is to get the title, Posted by is for the username
            parse_data = []
            for idx, ele in enumerate(list):
                print(idx)
                regex_ = "{}\:(.*).+?(?={})".format(ele, list[idx+1])
                tag = re.search(regex_, test).group(1)
                print(tag)
                ele = ele.replace('+\s+', ' ')
                if ele == "Description":
                    mail=findMails(ele)
                    phone = findPhones(ele)
                    website = findURL(ele)
                    parse_Data[mail] = mail
                    parse_Data[phone] = phone
                    parse_Data[website]= website
                parse_data[ele] = tag

                return parse_Data
       ### ajouter le titre et le nom d'utilisatueur
    #titre = driver.find_element_by_xpath("//font").text
    #parse_Data.append(titre)
    #id_user = driver.find_element_by_xpath("//td[@class='text-center']")
    #parse_Data.append(id_user)

def findMails(string):
    '''Récupère des adresses emails dans une chaine de caractère'''
    result = re.findall("\\b[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*(?:[\s\[\(])*(?:@|at)(?:[\s\]\)])*(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", string)
    return result

def findPhones(string):
    '''Récupère les numéros internationaux avec des espaces, /, - ou concatené'''
    result = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", string)
    return result

def findURL(string):
    '''Récupère les URL dans une page (utile lorsque les liens n'ont pas de balises <a href>). Attention, uniquement les liens "HTTP(S) ou www."!'''
    result = re.findall("(\\b(?:HTTP[S]?://|www\.)[\w\d\-\+&@#/%=~_\|\$\?!:,\.]{2,}[\w\d\+&@#/%=~_\|\$]*)", string, re.IGNORECASE)
    return result

main()

        import pdb; pdb.set_trace()
