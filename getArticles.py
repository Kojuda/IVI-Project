#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues
# creation: 15.10.2020

import time, json, sys, os, subprocess, re, csv
from lxml import html #pip install lxml cssselect
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   

from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressource
from ressources.db import *




#Ouverture de adpost_parsing.csv
# with open('./results/getcountries/adpost_parsing.csv', 'rb') as csvfile:
#     csv_reader = csv.reader(csvfile, delimiter=';')
#     for row in csv_reader:
#         driver.get(str(raw[0])

def check_exists_by_xpath(browser, xpath):
    try:
        browser.driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def saveData(browser, path):
    '''Fonction pour l'exemple qui enregistre le code client, la capture d'écran et code serveur'''
    browser.clientCode(path+'_clientCode.html')
    browser.screenshot(path+'_screenshot.png', width=1080) #on fixe la largeur de la fenêtre avec width
    #browser.serverCode(path+'_serverCode.html')
    #browser.driver.execute_script("window.history.go(-1)")

def getbirds(browser, url) :   
    """Go to bird section"""
    url = url.strip("/") + "/pets/Birds/"
    info = browser.get(url)
    info['actions'].append("info = browser.get(url)")
    return info

def getads(browser, session) :
    """Go through all pages to collect articles' urls"""
    #When the next button disappears at the end 
    counter=0
    while check_exists_by_xpath(browser, "//input[@name=\"button_hits_seen\"]") or counter!=1 :
        for ad in browser.driver.find_elements_by_xpath('//div[@class="row clearfix"]') :
            ad_number = ad.find_element_by_xpath(".//input[@type=\"checkbox\"]/@name")
            url = ad.find_element_by_xpath(".//a/@href")
            #Add the entry in the database
            Urls_ads(url=url, ad_number=ad_number).insertURL(session)
        counter+=1
        browser.driver.find_element_by_xpath("//input[@name=\"button_hits_seen\"]").click()



if __name__ == '__main__':

     #~~~~~~~~~~~~~~~ Configuration ~~~~~~~~~~~~~~~#
    url = "https://www.adpost.com/us/"
    filename_prefix = 'urlArticles'
    path = './results/getArticles/'

    browser = Firefox(tor=False, headless=True)
    doc = Documentation(driver=browser.driver)

    #~~~~~~~~~~~~~~~ First page of ads ~~~~~~~~~~~~~~~#


    info = getbirds(browser, url)
    doc.info['selenium'] = []
    doc.info['selenium'].append(info)
    doc.addlog("info = getbirds(browser, url)")
    browser.driver.find_element_by_xpath('//option[contains(text(), "FOR SALE / ADOPTION:")]').click()
    doc.addlog("browser.driver.find_element_by_xpath(\'//button[@name=\"login\"]\').click())")
    browser.driver.find_element_by_xpath('//option[contains(text(), "Birds")]').click()
    doc.addlog("browser.driver.find_element_by_xpath(\'//option[contains(text(), \"Birds\")]\').click()")

    saveData(browser, path+filename_prefix)

    getads(browser, session)
    #~~~~~~~~~~~~~~~ Catch'em all ~~~~~~~~~~~~~~~#


    # ~~~~~~~~~~~~~~~ Documentation - enregistrement ~~~~~~~~~~~~~~~ #
    with open('./results/getArticles/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

    # ~~~~~~~~~~~~~~~ Shut down the webdriver ~~~~~~~~~~~~~~~ #

    browser.driver.quit()

#countryButton = driver.findElement(str(raw[1])).click();
#countryButton.click();

#Ecrire le résultat
#with open('./results/getcountries/test', 'wb') as f:
#    f.write(str(doc).encode('utf-8'))
