#!/usr/bin/env python
# coding=utf-8
# author: L. Rodrigues
# creation: 15.10.2020

import time, json, sys, os, subprocess, re, csv
from lxml import html #pip install lxml cssselect
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ressources.webdriver import Chrome, Firefox # fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressource
from ressources.db import *
from ressources.project_utils import mapping_countries, map_country


def check_exists_by_xpath(webelement, xpath): 
    """Check whether exist"""
    try:
        webelement.find_element_by_xpath(xpath)
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

    #No need to wait between requests, it is on the same page, just javascript
    while check_exists_by_xpath(browser.driver, "//input[@name=\"button_hits_seen\"]")  :
        for ad in browser.driver.find_elements_by_xpath('//div[@class="row clearfix"][@style]') :
            #The website is inconsistent, there is tag without ad
            ad_number = ad.find_element_by_xpath(".//input[@type=\"checkbox\"]").get_attribute("name") 
            url = ad.find_element_by_xpath(".//a").get_attribute("href") 
            #Add the entry in the database
            country= map_country(browser.driver.current_url)
            entry=Urls_ads(url=url, ad_number=int(ad_number), country_id=country)
            entry.insertURL(session)
            entry.update(session)
        #When the next button disappears at the end 
        browser.driver.find_element_by_xpath("//input[@name=\"button_hits_seen\"]").click()



if __name__ == '__main__':

     #~~~~~~~~~~~~~~~ Configuration ~~~~~~~~~~~~~~~#
    url = "https://www.adpost.com/us/"
    filename_prefix = 'urlArticles'
    path = './results/getArticles/'

    browser = Firefox(tor=False, headless=True)
    doc = Documentation(driver=browser.driver)

    #~~~~~~~~~~~~~~~ Catch'em all ~~~~~~~~~~~~~~~#
    for row in session.query(Country).all():
        url = row.url

        info = getbirds(browser, url)
        doc.info['selenium'] = []
        doc.info['selenium'].append(info)
        doc.addlog("info = getbirds(browser, url)")
        
        browser.driver.find_element_by_xpath('//option[contains(text(), "FOR SALE / ADOPTION:")]').click()
        doc.addlog("browser.driver.find_element_by_xpath(\'//button[@name=\"login\"]\').click())")
        
        browser.driver.find_element_by_xpath('//option[contains(text(), "Birds")]').click()
        doc.addlog("browser.driver.find_element_by_xpath(\'//option[contains(text(), \"Birds\")]\').click()")

        saveData(browser, path+filename_prefix)
        doc.addlog("saveData(browser, path+filename_prefix)")

        getads(browser, session)
        doc.addlog("getads(browser, session)")

    # ~~~~~~~~~~~~~~~ Documentation - enregistrement ~~~~~~~~~~~~~~~ #
    with open('./results/getArticles/'+filename_prefix+'_documentation.json', 'wb') as f:
        f.write(str(doc).encode('utf-8'))

    # ~~~~~~~~~~~~~~~ Shut down the webdriver ~~~~~~~~~~~~~~~ #

    browser.driver.quit()





#Ouverture de adpost_parsing.csv
# with open('./results/getcountries/adpost_parsing.csv', 'rb') as csvfile:
#     csv_reader = csv.reader(csvfile, delimiter=';')
#     for row in csv_reader:
#         driver.get(str(raw[0])

#countryButton = driver.findElement(str(raw[1])).click();
#countryButton.click();

#Ecrire le résultat
#with open('./results/getcountries/test', 'wb') as f:
#    f.write(str(doc).encode('utf-8'))
