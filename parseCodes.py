#!/usr/bin/env python
# coding=utf-8
# author: L.Lopez and D.Kohler
# creation: 25.10.2020
# But: parser le code client des publications de vente

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Ads_Codes
import lxml.html
# import pdb
# import pdb; pdb.set_trace()

champs = ['Reply to Ad','Category', 'Ad Number','Date Posted','Description', 'Breed','Age', 'Sex','Primary Color', 'Secondary Color','Advertiser','Price','Payment Forms','Estimated Shipping','Posted By','Contact Information','Name', 'Company', 'Address', 'Postal Code',\
'Zip Code', 'Post Code', 'State > District', 'State > City','City', 'State > County','Province > County', 'Province > City','Region > County','County','Region', 'State > Metro', 'Country', 'Phone', 'Email','Forum']

dict_champ = {'Title' : None, 'Category' : None, 'Ad Number' : None,
'Date Posted' : None,'Description' : None, 'Breed' : None,
'Age' : None, 'Sex' : None,'Primary Color' : None,
 'Secondary Color' : None,'Advertiser' : None,
 'Price' : None,'Payment Forms' : None,'Estimated Shipping' : None,
 'Pseudo' : None,'Contact Information' : None,'Name' : None,
  'Company' : None, 'Address' : None, 'Postal Code' : None,
'Zip Code' : None, 'Post Code' : None, 'State > District' : None,
 'State > City' : None,'City' : None, 'State > County' : None,
 'Province > County' : None, 'Province > City' : None,'Region > County' : None,
 'County' : None,'Region' : None, 'State > Metro' : None,
  'Country' : None, 'Phone' : None, 'Email' : None, "Link Vendor" : None}

def check_exists_by_xpath(tag, xpath): 
    """Check whether exist"""
    try:
        tag.xpath(xpath)[0]
        return True
    except :
        return False

def get_champs(dic, html_object) :
    """Iterate through the tag containing the fields of the ad. The function fills a dictionary containing
    the label of the possible fields. If the label is not found, the value of the key remains None. """

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
                check_exists_by_xpath(row, "./div/div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']")
                if check_exists_by_xpath(row, "./div/div/div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']") :
                    vendor_left=row.xpath("./div/div/div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']")[0]
                    dic["Link Vendor"]=vendor_left.xpath("./div/table/tbody/tr/td/a[@style=\'color: #fff;\']/@href")[0]
                    dic["Pseudo"]=vendor_left.xpath("./div/table/tbody/tr/td/a[@style=\'color: #fff;\']/text()")[0].strip(" ")
                    #Unique xpath at this level to obtain the list of row elements
                    #vendor_entries=row.xpath("./div[@class=\'col-md-9 col-sm-9 col-xs-12 z-ad-func-obj\']")
                    vendor_entries=row.xpath("./div/div[2]/div[2]/div[@class=\'row\']")
                    for row_vendor in vendor_entries :
                        #The categorie --> Ex : Address/Name/Postal Code
                        categorie=row_vendor.xpath("./div[1]/b/text()")[0].strip(" :")
                        #Check the categorie
                        if categorie in dic.keys() :
                            #Get the entry of this categorie
                            field=row_vendor.xpath("string(./div[2]/text())").strip(" \n")
                            if field != "" :
                                dic[categorie]=field
        #Here the special case of the description
        elif check_exists_by_xpath(row, "./div[@class=\'col-md-4\']/b") :
            if row.xpath("./div[@class=\'col-md-4\']/b")[0].text == "Description: " :
                if check_exists_by_xpath(row, "./following::div[1]") :
                    description=row.xpath("string(./following::div[1])").replace("\t", " ").replace("\n", " ").replace("  ", " ").strip(" ")
                    dic["Description"]=description
        #All other fields
        elif check_exists_by_xpath(row, "./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b"):
            #The categorie --> Ex : Address/Name/Postal Code
            categorie=row.xpath("./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b")[0].text
            if type(categorie) == str:
                categorie = categorie.strip(" :")
            else:
                print("nonetype")
            #Check the categorie
            if categorie in dic.keys() :
                #Get the entry of this categorie
                if check_exists_by_xpath(row, "./div[2]") :
                    #field=row.xpath("./div[@class=\'col-md-8 col-sm-7 col-xs-6 z-ad-func-obj\']/text()")[0].strip(" ")
                    field=row.xpath("string(./div[2])").strip(" \t\n")
                if field != "" :
                    dic[categorie]=field
                #Allow to check if a field has been assigned without the 2 conditions are True
                field="ERROR"
        else :
            print("Pass\n")

    return dic

def create_entry(dic, entry_ads_codes) :
    entry = Parse_ads(
        title = dic["Title"],
        ad_id = entry_ads_codes.ad_id,
        ad_number = entry_ads_codes.ad_number,
        category = dic["Category"],
        description = dic["Description"],
        breed = dic["Breed"],
        age = dic["Age"],
        sex = dic["Sex"],
        primary_color = dic["Primary Color"],
        secondary_color = dic["Secondary Color"],
        advertiser = dic["Advertiser"],
        price = dic["Price"],
        payment_forms = dic["Payment Forms"],
        estimated_shipping = dic["Estimated Shipping"],
        pseudo = dic["Pseudo"],
        contact_information = dic["Contact Information"],
        name = dic["Name"],
        company=  dic["Company"],
        zip = get_zip(dic),
        city = get_city(dic),
        state = get_state(dic),
        county = get_county(dic),
        country= dic["Country"],
        region = get_region(dic),
        province = get_province(dic),
        email = dic["Email"],
        phone = dic["Phone"],
        redirect_website= dic["Link Vendor"]
    )
    return entry

def get_zip(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["Post Code"] is None :
        output=dic["Post Code"]
    elif not dic["Zip Code"] is None :
        output=dic["Zip Code"]
    else :
        output=None
    return output

def get_state(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["State > City"] is None : #if its not None do something
        if not re.findall("(.*)>.*",dic["State > City"]) == []: #To catch error if list is empty
            output = re.findall("(.*)>.*",dic["State > City"])[0].strip(" ")
        else:
            output = None
    elif not dic["State > County"] is None :
        if not re.findall("(.*)>.*",dic["State > County"]) == []:
            output = re.findall("(.*)>.*",dic["State > County"])[0].strip(" ")
        else:
            output = None
    elif not dic["State > Metro"] is None :
        if not re.findall("(.*)>.*",dic["State > Metro"]) == []:
            output = re.findall("(.*)>.*",dic["State > Metro"])[0].strip(" ")
        else:
            output = None
    elif not dic["State > District"] is None :
        if not re.findall("(.*)>.*",dic["State > District"]) == []:
            output = re.findall("(.*)>.*",dic["State > District"])[0].strip(" ")
        else:
            output = None
    else :
        output=None
    
    return output

def get_county(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["County"] is None :
        output=dic["County"]
    elif not dic["Region > County"] is None :
        if not re.findall(".*>(.*)",dic["Region > County"]) == []:
            output=re.findall(".*>(.*)",dic["Region > County"])[0].strip(" ")
        else:
            output = None
    elif not dic["State > County"] is None :
        if not re.findall(".*>(.*)",dic["State > County"]) == []:
            output=re.findall(".*>(.*)",dic["State > County"])[0].strip(" ")
        else:
            output = None
    elif not dic["Province > County"] is None :
        if not re.findall(".*>(.*)",dic["Province > County"]) == []:
            output=re.findall(".*>(.*)",dic["Province > County"])[0].strip(" ")
        else:
            output = None
    else :
        output=None
    return output


def get_city(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["City"] is None :
        output=dic["City"]
    elif not dic["State > City"] is None :
        output=re.findall(".*>(.*)",dic["State > City"])[0].strip(" ")
    elif not dic["Province > City"] is None :
        output=re.findall(".*>(.*)",dic["Province > City"])[0].strip(" ")
    else :
        output=None
    return output

def get_region(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["Region"] is None :
        output=dic["Region"]
    elif not dic["Region > County"] is None :
        output=re.findall("(.*)>.*",dic["Region > County"])[0].strip(" ")
    else :
        output=None
    return output

def get_province(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["Province > City"] is None :
        output=re.findall("(.*)>.*",dic["Province > City"])[0].strip(" ")
    elif not dic["Province > County"] is None :
        output=re.findall("(.*)>.*",dic["Province > County"])[0].strip(" ")
    else :
        output=None
    return output









if __name__ == '__main__':
    #to do it in all the files of client code

    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
    
    counter=0
    path_result=r'C:\Users\Jasmin\Documents\Switchdrive\results\getCodes\codes\\'
    for row in session.query(Ads_Codes).filter_by(status=0):
        #Skip if already exists
        if session.query(exists().where(Parse_ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            #TEST
            dic_champs=dict_champ.copy()
            filename=row.client_code
            objet = lxml.html.parse(f"{path_result}{filename}").getroot()
            dic_champs = get_champs(dic_champs, objet)
            entry = create_entry(dic_champs, row)
            entry.insertParse_ads(session)
            #row.update(session)







            counter+=1
    #before: f'./results/getCodes/documentation/
    # for jasmin: f'C:/Users/Jasmin/Documents/Switchdrive/results/getCodes/documentation/'
    print(date_parsing)
    with open(f'C:/Users/Jasmin/Documents/Switchdrive/results/getCodes/documentation/{date_parsing}_documentation.json', 'wb') as f:
                f.write(str(doc).encode('utf-8'))



















































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
