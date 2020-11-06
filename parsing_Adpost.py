#!/usr/bin/env python
# coding=utf-8
# author: L.Lopez
# creation: 25.10.2020
# But: parser les pages web

import time, json, random, re, datetime, os
from ressources.webdriver import Chrome, Firefox #fichier selenium_driver.py à placer dans le même dossier que votre script
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressources
from selenium import webdriver
from ressources.db import Parse_ads, session, Ads_Codes
import lxml.html
# import pdb
# import pdb; pdb.set_trace()

champs = ['Reply to Ad','Category', 'Ad Number','Date Posted','Description', 'Breed','Age ', 'Sex','Primary Color', 'Secondary Color','Advertiser','Price','Payment Forms','Estimated Shipping','Posted By','Contact Information','Name', 'Company', 'Address', 'Postal Code',\
'Zip Code', 'Post Code', 'State > District', 'State > City','City', 'State > County','Province > County', 'Province > City','Region > County','County','Region', 'State > Metro', 'Country', 'Phone', 'Email','Forum']

dict_champ = {'Title' : None, 'Category' : None, 'Ad Number' : None,
'Date Posted' : None,'Description' : None, 'Breed' : None,
'Age ' : None, 'Sex' : None,'Primary Color' : None,
 'Secondary Color' : None,'Advertiser' : None,
 'Price' : None,'Payment Forms' : None,'Estimated Shipping' : None,
 'Pseudo' : None,'Contact Information' : None,'Name' : None,
  'Company' : None, 'Address' : None, 'Postal Code' : None,
'Zip Code' : None, 'Post Code' : None, 'State > District' : None,
 'State > City' : None,'City' : None, 'State > County' : None,
 'Province > County' : None, 'Province > City' : None,'Region > County' : None,
 'County' : None,'Region' : None, 'State > Metro' : None,
  'Country' : None, 'Phone' : None, 'Email' : None,'Forum' : None, "Link Vendor" : None}

def check_exists_by_xpath(tag, xpath): 
    """Check whether exist"""
    try:
        tag.xpath(xpath)
    except :
        return False
    return True

def parse(filename):
    objet = lxml.html.parse(filename).getroot()
    stateScript = objet.xpath("//script[@id='state']")
    data = re.search(r'window.__INITIAL_STATE__\s*=\s*(.*)\s*', stateScript[0].text, flags=re.DOTALL)[1]
    data = re.sub('\s+',' ', data)
    data = json.loads(data)['detail']
    result = {
        'annonce_id': valeur(data, 'annonce_id'),
        'auteur_id': valeur(data, 'auteur_id'),
        'date': valeur(data, 'date'),
        'categorie': valeur(data, 'categories'),
        'titre': valeur(data, 'titre'),
        'description': valeur(data, 'description'),
        'adresse': valeur(data, 'adresse'),
        'ville': valeur(data, 'ville'),
        'prix': valeur(data, 'prix'),
        'phone': valeur(data, 'phone'),
        'website': valeur(data, 'url')
    }
    return result

def get_champs(dic, html_object) :
    #Get the xpath of the title in the dev browser with right click
    dic["Title"]=html_object.xpath("//html/body/div/div/div[3]/div[1]/div[5]/div/div[2]/div/table/tbody/tr/th/font")[0].text
    #Get the list of champs from the tag containing the whole ad
    ad=html_object.xpath("///html/body/div/div/div[3]/div[1]/div[5]/div/div[3]/div[2]/div/div/div[@class=\"row\"]")
    #Each row can have a entry (Or not !). We iterate over all rows to extract entry
    #Special case : Description entry has its content in the next row ! And the row that contains "Posted by" has
    #its own list of rows, we need to iterate once again in this list
    for row in ad :
        #Here we iterate through the vendor information
        #Avoid bug if does not exist
        if check_exists_by_xpath(row, "./div/div[@style=\'font-size:14px\']/b") :
            if row.xpath("./div/div[@style=\'font-size:14px\']/b")[0].text == "Posted By: " :
                #Left side of the pane concerning the vendor information
                vendor_left=row.xpath("./div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']")[0]
                dic["Link Vendor"]=vendor_left.xpath("./a[@style=\'color: #fff;\']/@href")[0]
                dic["Pseudo"]=vendor_left.xpath("./a[@style=\'color: #fff;\']/@href")[0].text
                #Unique xpath at this level to obtain the list of row elements
                vendor_entries=row.xpath("./div[@class=\'col-md-9 col-sm-9 col-xs-12 z-ad-func-obj\']")
                for row_vendor in vendor_entries :
                    #The categorie --> Ex : Address/Name/Postal Code
                    categorie=row_vendor.xpath("./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b")[0].text.strip(" :")
                    #Check the categorie
                    if categorie in dic.keys() :
                        #Get the entry of this categorie
                        field=row_vendor.xpath("./div[@class=\'col-md-8 col-sm-7 col-xs-6 z-ad-func-obj\']/b")[0].text.strip(" ")
                        dic[categorie]=field
        #Here the special case of the description
        elif check_exists_by_xpath(row, "./div[@class=\'col-md-4\']/b") :
            if row.xpath("./div[@class=\'col-md-4\']/b")[0].text == "Description: " :
                description=row.xpath("./div[@class=\'col-md-4\']/following-sibling::div[@class=\'col-md-12\']")[0].text
                dic[Description]=description
        #All other fields
        elif check_exists_by_xpath(row, "./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b") :
            #The categorie --> Ex : Address/Name/Postal Code
            categorie=row.xpath("./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b")[0].text.strip(" :")
            #Check the categorie
            if categorie in dic.keys() :
                #Get the entry of this categorie
                field=row.xpath("./div[@class=\'col-md-8 col-sm-7 col-xs-6 z-ad-func-obj\']/b")[0].text.strip(" ")
                dic[categorie]=field
        else :
            print("Pass\n")


    return dic

if __name__ == '__main__':
    counter=0
    path_result="./results/getCodes/codes/"
    for i in session.query(Ads_Codes).filter_by(status=0):
        #TEST
        if counter > 1 :
            break
        dic_champs=dict_champ.copy()
        filename=i.client_code
        objet = lxml.html.parse(f"{path_result}{filename}").getroot()
        get_champs(dic_champs, objet)






        counter+=1



















































    # driver = webdriver.Firefox(executable_path=r"webdrivers/geckodriver")
    # set=driver.get("https://www.adpost.com/uk/pets/81040/")
    # balise_b = driver.find_element_by_xpath("//b")
    # test = balise_b.find_element_by_xpath("./..").find_element_by_xpath("//div").text
    # test = test.strip()
    # test = test.replace("\n"," ").replace(": "," ").replace("click above for more info on this user","").replace("Please quote Adpost when calling","").replace("click to view 1 more image","").replace("click to view 2 more images","")
    # #import pdb; pdb.set_trace()




    

    # list_mot = ['Reply to Ad','Category', 'Ad Number','Date Posted','Description', 'Breed','Age ', 'Sex','Primary Color', 'Secondary Color','Advertiser','Price','Payment Forms','Estimated Shipping','Posted By','Contact Information','Name', 'Company', 'Address', 'Postal Code',\
    # 'Zip Code', 'Post Code', 'State > District', 'State > City','City', 'State > County','Province > County', 'Province > City','Region > County','County','Region', 'State > Metro', 'Country', 'Phone', 'Email','Forum']

    # clean_list = [x for x in list_mot if x in test] #comprehensive list / liste de mot réelleemnt présent sur la page parmi toutes les possibilités de list_mot

    # if 'Province > City' in test or 'State > City' in test:
    #     clean_list.remove('City')

    # if 'Region > County' in test or 'State > County' in test or 'Province > County' in test:
    #     clean_list.remove('County')
    #     clean_list.remove('Region')


    # parse_data = {}
    # #Récupérer les mots au milieu des termes de clean_list en utilisant regex
    # for idx, ele in enumerate(clean_list):
    #     if idx == len(clean_list)-1:
    #         break
    #     else:
    #         regex_ = "{}(.*){}".format(ele, clean_list[idx+1])
    #         #import pdb; pdb.set_trace()
    #         tag = re.search(regex_, test).group(1)
    #         #import pdb; pdb.set_trace()
    #         parse_data[ele] = tag
    #         test = test.replace(tag, "")



    # """
    # rechercher le numéro de téléphone, l'adresse email ainsi qu'un site web dans le champ "Description" et ajout de ces informations au dictionnairepartie pour extraire le mail, le phone et website de la description

    # description = parse_data.get('Description')
    # email, phone, website = None, None, None
    # if description:

    #     email_regex = re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",description)
    #     if email_regex:
    #         email = email_regex.group(1)
    #         print (email)

    #     phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",description)
    #     if phone_regex:
    #         phone = phone_regex.group(1)
    #         print (phone)

    #     website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))",description)
    #     if website_regex:
    #         website = website_regex.group(1)
    #         print (website)


    #     parse_data['Email'] = email
    #     parse_data['phone'] = phone
    #     parse_data['redirect_website'] = website
    #     del parse_data['Description']
    #     """

    # new_key = "title"
    # old_key = "Reply to Ad"
    # parse_data[new_key]= parse_data.pop(old_key)
    # new_key = "category"
    # old_key = "Category"
    # parse_data[new_key]= parse_data.pop(old_key)




    # state = ('State > District', 'State > City','State > County','Province > County','Province > City', 'Region > County', 'Region','County', 'State > Metro')
    # for x in state:
    #     if x in parse_data:
    #         parse_data["State"] =parse_data.pop(x)

    # zip_code = ("Postal Code", "Zip Code", "Post Code")
    # for y in zip_code:
    #     if y in parse_data:
    #         parse_data["Zip Code"] =parse_data.pop(y)

    # posted_by = ("Posted By", "Contact Information")
    # for z in posted_by:
    #     if z in parse_data:
    #         parse_data["Posted By"] =parse_data.pop(z)






    # """
    # print (parse_data)
    # if parse_data['Email'] == None or parse_data['phone'] == None or parse_data['redirect_website'] == None :
    #     del parse_data['Email']
    #     del parse_data['phone']
    #     del parse_data['redirect_website']

    #     #parse_data[new_key]= parse_data.pop(old_key)
    #     parse_data['Email'] = 'none'
    #     parse_data['phone'] = 'none'
    #     parse_data['redirect_website'] = 'none'
    # """






    # # partie sqlite
    # # Mettre à none les valeurs vide
    # list_database = ['title','category','Ad Number','Date Posted','Description','Breed','Age ','Sex','Primary Color','Secondary Color','Advertiser','Price', 'Payment Forms','Estimated Shipping','Posted By','Name','Zip Code','City','State','Country','Email','phone']
    # for mot in list_database:
    #     if mot not in parse_data:
    #         parse_data[mot] = 'none'
    # #import pdb; pdb.set_trace()



    # Parse_ads(title=parse_data.get('title'), category = parse_data.get('category'), ad_number = parse_data.get('Ad Number'), date_posted = parse_data.get('Date Posted'),description= parse_data.get('Description'), breed = parse_data.get('Breed'), age= parse_data.get('Age '), sex= parse_data.get('Sex'), primary_color = parse_data.get('Primary Color'),\
    # secondary_color= parse_data.get('Secondary Color'), advertiser= parse_data.get('Advertiser'), price= parse_data.get('Price'), payment_forms= parse_data.get('Payment Forms'), estimated_shipping= parse_data.get('Estimated Shipping'), posted_by = parse_data.get('Posted By'),\
    # name= parse_data.get('Name'), zip= parse_data.get('Zip Code'), city= parse_data.get('City'), state= parse_data.get('State'), country= parse_data.get('Country'), email= parse_data.get('Email'),phone = parse_data.get('phone')).insertParse_ads(session)

    # #import pdb; pdb.set_trace()
