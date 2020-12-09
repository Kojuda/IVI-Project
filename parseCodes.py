#!/usr/bin/env python
# coding=utf-8

"""Le script itère à travers la base de données pour parser les données de tous les codes clients récoltés sous les 
différents répertoires de la plateforme Adpost.com. Les données sont stockées dans la table "parse_codes" """

import time, json, random, re, datetime, os
from sqlalchemy.sql import exists
from ressources.documentation import Documentation 
from ressources.db import Parse_ads, session, Ads_Codes
import lxml.html

champs = ['Reply to Ad','Category', 'Ad Number','Date Posted','Description', 'Breed','Age', 'Sex','Primary Color', 'Secondary Color','Advertiser','Price','Payment Forms','Estimated Shipping','Posted By','Contact Information','Name', 'Company', 'Address', 'Postal Code',\
'Zip Code', 'Post Code', 'State > District', 'State > City','City', 'State > County','Province > County', 'Province > City','Region > County','County','Region', 'State > Metro', 'Country', 'Phone', 'Email','Forum']

#Global variable of all the possible fields. A copy of that is used to store
#the parsed information.
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

def check_exists_by_xpath(tag, xpath, doc, dic, realerror=True): 
    """Check whether exist, document error otherwise"""
    try:
        tag.xpath(xpath)[0]
        return True
    except :
        if realerror :
            doc.adderrorlog(f"{dic['Ad Number']} - Error on xpath = {xpath}")
        return False

def get_champs(dic, html_object, doc) :
    """Iterate through the tag containing the fields of the ad. The function fills a dictionary containing
    the label of the possible fields. If the label is not found, the value of the key remains None. """

    #Get the xpath of the title in the dev browser with right click
    if check_exists_by_xpath(html_object, "//html/body/div/div/div[3]/div[1]/div[5]/div/div[2]/div/table/tbody/tr/th/font", doc, dic) :
        dic["Title"]=html_object.xpath("//html/body/div/div/div[3]/div[1]/div[5]/div/div[2]/div/table/tbody/tr/th/font")[0].text
    else :
        #No ad found
        dic["Title"]="-1"
    #Get the list of champs from the tag containing the whole ad

    #TWO CASES : there is a picture in the ad or not. Difference of 1 tag since the field lists is at the same level that the photo
    #Picture
    if check_exists_by_xpath(html_object, "///html/body/div/div/div[3]/div[1]/div[5]/div/div[3]/div[2]/div/div/div[@class=\"row\"]", doc, dic, realerror=False) :
        ad=html_object.xpath("///html/body/div/div/div[3]/div[1]/div[5]/div/div[3]/div[2]/div/div/div[@class=\"row\"]")
    #No picture
    elif check_exists_by_xpath(html_object, "///html/body/div/div/div[3]/div[1]/div[5]/div/div[3]/div[1]/div/div/div[@class=\"row\"]", doc, dic) :
        ad=html_object.xpath("///html/body/div/div/div[3]/div[1]/div[5]/div/div[3]/div[1]/div/div/div[@class=\"row\"]")

    #Each row can have a entry (Or not !). We iterate over all rows to extract entry
    #Special case : Description entry has its content in the next row ! And the row that contains "Posted by" has
    #its own list of rows, we need to iterate once again in this list
    try :
        for row in ad :
            #Here we iterate through the vendor information
            if check_exists_by_xpath(row, "./div/div[@style=\'font-size:14px\']/b", doc, dic) :
                if row.xpath("./div/div[@style=\'font-size:14px\']/b")[0].text:
                    #Left side of the pane concerning the vendor information
                    if check_exists_by_xpath(row, "./div/div/div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']", doc, dic) :
                        vendor_left=row.xpath("./div/div/div[@class=\'col-md-3 col-sm-3 col-xs-12 z-ad-func-obj\']")[0]
                        dic["Link Vendor"]=vendor_left.xpath("./div/table/tbody/tr/td/a[@style=\'color: #fff;\']/@href")[0]
                        dic["Pseudo"]=vendor_left.xpath("./div/table/tbody/tr/td/a[@style=\'color: #fff;\']/text()")[0].strip(" ")
                        #Unique xpath at this level to obtain the list of row elements
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
            elif check_exists_by_xpath(row, "./div[@class=\'col-md-4\']/b", doc, dic) :
                if row.xpath("./div[@class=\'col-md-4\']/b")[0].text == "Description: " :
                    if check_exists_by_xpath(row, "./following::div[1]", doc, dic) :
                        description=row.xpath("string(./following::div[1])").replace("\t", " ").replace("\n", " ").replace("  ", " ").strip(" ")
                        dic["Description"]=description
            #All other fields
            elif check_exists_by_xpath(row, "./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b", doc, dic):
                #The categorie --> Ex : Address/Name/Postal Code
                categorie=row.xpath("./div[@class=\'col-md-4 col-sm-5 col-xs-6 z-ad-func-obj\']/b")[0].text
                if type(categorie) == str:
                    categorie = categorie.strip(" :")
                else:
                    print(f"Field empty : {dic['Ad Number']}\n")
                #Check the categorie
                if categorie in dic.keys() :
                    #Get the entry of this categorie
                    if check_exists_by_xpath(row, "./div[2]", doc, dic) :
                        field=row.xpath("string(./div[2])").strip(" \t\n")
                    if field != "" :
                        dic[categorie]=field
                    #Allow to check if a field has been assigned without the 2 conditions are True
                    field="ERROR"
            else :
                #Empty row
                print("Pass\n")
    except :
        tmp=dic["Ad Number"]
        doc.adderrorlog(f"{tmp} - Error no ad detected")

    return dic

def create_entry(dic, entry_ads_codes) :
    """Function to create an SQL entry according to the dict fulfills with
    the parsed information and the raw line from the SQL database we're iterating
    through. """
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
        if not re.findall(".*>(.*)",dic["State > City"]) == []:
            output=re.findall(".*>(.*)",dic["State > City"])[0].strip(" ")
        else:
            output = None
    elif not dic["Province > City"] is None :
        if not re.findall(".*>(.*)",dic["Province > City"]):
            if not re.findall(".*>(.*)",dic["Province > City"]) == []:
                output=re.findall(".*>(.*)",dic["Province > City"])[0].strip(" ")
            else:
                output = None
        else:
            output = None
    else :
        output=None
    return output

def get_region(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["Region"] is None :
        output=dic["Region"]
    elif not dic["Region > County"] is None :
        if not re.findall("(.*)>.*",dic["Region > County"]) == []:
            output=re.findall("(.*)>.*",dic["Region > County"])[0].strip(" ")
        else:
            output= None
    else:
        output=None
    return output

def get_province(dic) :
    """Function to get an information that might be in several fields"""
    if not dic["Province > City"] is None :
        if not re.findall("(.*)>.*",dic["Province > City"])==[]:
            output=re.findall("(.*)>.*",dic["Province > City"])[0].strip(" ")
        else:
            output = None
    elif not dic["Province > County"] is None :
        if not re.findall("(.*)>.*",dic["Province > County"])==[]:
            output=re.findall("(.*)>.*",dic["Province > County"])[0].strip(" ")
        else:
            output= None
    else :
        output=None
    return output




if __name__ == '__main__':

    #Documentation
    cT = datetime.datetime.now()
    date_parsing = f"{str(cT.year)}-{str(cT.month)}-{str(cT.day)}_{str(cT.hour)}-{str(cT.minute)}"
    doc = Documentation()
   
    path_result='./results/getCodes/codes/'

    #Iterate through client codes
    for row in session.query(Ads_Codes).filter_by(status=0): #status=0
        #Skip if already exists
        if session.query(exists().where(Parse_ads.ad_id == row.ad_id)).scalar():
            pass
        else:
            #Copy the global variable containing the fields in the ad
            dic_champs=dict_champ.copy()
            filename=row.client_code
            #Set it up to use later
            dic_champs["Ad Number"]=row.ad_number
            #Obtain the HTML object
            objet = lxml.html.parse(f"{path_result}{filename}").getroot()
            #The main function that parses the HTML object
            dic_champs = get_champs(dic_champs, objet, doc)
            entry = create_entry(dic_champs, row)

            session.commit()
            entry.insertParse_ads(session)
            row.update(session)

        #Write the doc several time to lost the documentation whether the script fails.
        with open(f'./results/parseCodes/documentation/{date_parsing}_documentation.json', 'wb') as f:
                    f.write(str(doc).encode('utf-8'))
