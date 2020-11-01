#!/usr/bin/env python
# coding=utf-8
# author: L.Lopez
# creation: 25.10.2020
# But: parser les pages web

import time, json, random
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from ressources.db import Parse_ads, session
from selenium import webdriver
import re
import pdb

driver = webdriver.Firefox(executable_path=r"webdrivers/geckodriver")
set=driver.get("https://www.adpost.com/us/pets/553087/")

balise_b = driver.find_element_by_xpath("//b")
test = balise_b.find_element_by_xpath("./..").find_element_by_xpath("//div").text
test = test.strip()
test = test.replace("\n"," ")
print (test)



liste = ['Reply to Ad','Category', 'Ad Number', 'Description', 'Breed','Age', 'Sex', 'Advertiser','Email','Forum']
clean_list = [x for x in liste if x in test] #comprehensive list

parse_data = {}
for idx, ele in enumerate(clean_list):
    if idx == len(clean_list)-1:
        break
    else:
        regex_ = "{}(.*){}".format(ele, clean_list[idx+1])
        tag = re.search(regex_, test).group(1)
        parse_data[ele] = tag
        #parse_data.append(tag)
        print (parse_data)


description = parse_data.get('Description')
email, phone = None, None
if description:
    #regex
    #phone = re.findall()
    email_regex = re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",description)
    if email_regex:
        email = email_regex.group(1)
        print (email)
    #if phone_regex:
        #phone = phone.group(1)

    #parse_data['phone'] = phone
    parse_data['Email'] = email
    del parse_data['Description']

    print(parse_data)

    #if ele == "Description":
                    #mail=findMails(ele)
                    #parse_data.append(mail)

    #if test.find(ele) != -1:  #https://www.programiz.com/python-programming/methods/string/find
        #continue
    #else:
        #idx += 1
        #parse_data.append("None")
        #import pdb; pdb.set_trace()



print (parse_data)
#essai= ["la","2","4"]
#Parse_ads(title=essai[0], category=essai[1], ad_number= essai[2]).insertParse_ads(session)


def findMails(string):
    '''Récupère des adresses emails dans une chaine de caractère'''
    result = re.findall(r'+', str)
    #result = re.findall("\\b[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*(?:[\s\[\(])*(?:@|at)(?:[\s\]\)])*(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", string)

    return result
    #regex_ = "{}\:(.*).+?(?={})".format(ele, list[idx+1]
