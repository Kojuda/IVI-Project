#!/usr/bin/env python
# coding=utf-8
# author: L.Lopez
# creation: 25.10.2020
# But: parser les pages web

import time, json, random
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from selenium import webdriver
from ressources.db import Parse_ads, session
import re
import pdb

driver = webdriver.Firefox(executable_path=r"webdrivers/geckodriver")
set=driver.get("https://www.adpost.com/us/pets/553216/")

balise_b = driver.find_element_by_xpath("//b")
test = balise_b.find_element_by_xpath("./..").find_element_by_xpath("//div").text
test = test.strip()
test = test.replace("\n"," ").replace(": "," ").replace("click above for more info on this user","").replace("Please quote Adpost when calling","").replace("click to view 1 more image","").replace("click to view 2 more images","")
#test = test.replace(":"," ")
#test = test.replace("click above for more info on this user","")
#test = test.replace("Please quote Adpost when calling","")
#test = test.replace("click to view 1 more image","")
#test = test.replace("click to view 2 more images","")
#res = test.replace('a', '%temp%').replace('b', 'a').replace('%temp%', 'b')
#print (test)
#import pdb; pdb.set_trace()





list_mot = ['Reply to Ad','Category', 'Ad Number','Date Posted','Description', 'Breed','Age', 'Sex',' Primary Color', 'Secondary Color','Advertiser','Price','Payment Forms','Estimated Shipping','Posted By','Contact Information',' Name', 'Company', 'Address', 'Postal Code',\
'Zip Code', 'Post Code', 'State > District', 'State > City','City', 'State > County','Province > County', 'Province > City','Region > County','County','Region', 'State > Metro', 'Country', 'Phone', 'Email','Forum']

clean_list = [x for x in list_mot if x in test] #comprehensive list / liste de mot réelleemnt présent sur la page parmi toutes les possibilités de list_mot
#import pdb; pdb.set_trace()

if 'Province > City' in test or 'State > City' in test: #if "x" in test or "y" in test or "z" in test: print(x)
    clean_list.remove('City')
#import pdb; pdb.set_trace()
if 'Region > County' in test or 'State > County' in test or 'Province > County' in test:
    clean_list.remove('County')
#import pdb; pdb.set_trace()

parse_data = {}
for idx, ele in enumerate(clean_list):
    if idx == len(clean_list)-1:
        break
    else:
        regex_ = "{}(.*){}".format(ele, clean_list[idx+1])
        tag = re.search(regex_, test).group(1)
        parse_data[ele] = tag
        #print (parse_data)

# rechercher le numéro de téléphone, l'adresse email ainsi qu'un site web dans le champ "Description"
# et ajout de ces informations au dictionnaire
description = parse_data.get('Description')
email, phone, website = None, None, None
if description:

    email_regex = re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",description)
    if email_regex:
        email = email_regex.group(1)
        print (email)

    phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",description)
    if phone_regex:
        phone = phone_regex.group(1)
        print (phone)

    website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))",description)
    if website_regex:
        website = website_regex.group(1)
        print (website)


    parse_data['Email'] = email
    parse_data['phone'] = phone
    parse_data['redirect_website'] = website
    del parse_data['Description']
    new_key = "title"
    old_key = "Reply to Ad"
    parse_data[new_key]= parse_data.pop(old_key)
    state = ('State > District', 'State > City','State > County','Province > County','Province > City', 'Region > County', 'Region','County', 'State > Metro')
    for x in state:
        if x in parse_data:
            parse_data["State"] =parse_data.pop(x)

    #for e in ['cc', 'dd',...]:
    #parse_data["Canton"] =parse_data.pop(e)
    #parse_data["Canton"] = parse_data.pop('State > County' or )
    #import pdb; pdb.set_trace()

    #print(parse_data)


#Est ce que qqn est sur le GIT ? je n'arrive plus commit

print (parse_data)
# sqlite

Parse_ads(title=parse_data.get('title'), ad_number= parse_data.get('Ad Number'), category= parse_data.get('Category'), breed = parse_data.get('Breed'), age = parse_data.get('Age'), sex= parse_data.get('Sex'), primary_color = parse_data.get('Primary Color'), \
secondary_color= parse_data.get('Secondary Color'), advertiser= parse_data.get('Advertiser'), price= parse_data.get('Price'), payment_forms= parse_data.get('Payment Forms'), estimated_shipping= parse_data.get('Estimated Shipping'), posted_by = parse_data.get('Username'), name= parse_data.get('Name'),\
zip= parse_data.get('Postal Code'), city= parse_data.get('City'), state= parse_data.get('State'), country= parse_data.get('United States'), email= parse_data.get('Email'), phone = parse_data.get('phone'), redirect_website= parse_data.get('redirect_website')).insertParse_ads(session)
