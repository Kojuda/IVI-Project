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

            list = ['Category', 'Ad+\s+Number', 'Description'] # c'est à continuer avec les autres éléments à parser
            parse_data = []
            for idx, ele in enumerate(list):
                print(idx)
                import pdb; pdb.set_trace()
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
