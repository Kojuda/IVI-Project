
"""
Ce script permet de prendre les données brutes parsées dans la table "parse_ads" pour parser cette fois le texte de 
l'annonce est retiré des informations pertinentes. Certains champs sont aussi rendus plus propres afin de pouvoir être
manipulés par un outil d'analyse. (e.g. le champ concernent l'argent)
"""

from ressources.db import session, Parse_ads, Vendor_analyse, Ads_clean, Classification_3_Ads
import re

currency_regex=["$","£","h","k","rm","php","p","rs","hd","hkd","sgd","sd","s$"] #currencies which will be searched
transform_to_dollar =["1","1.33","0.13","0.28","0.24","0.021","0.021","0.014","0.13","0.13","0.74","0.74","0.74"] #transform currency to $ (USD)

def get_email(row):
    """takes row of ad_parse as entry, returns email found in description"""
    email_regex =re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",row.description)
    if email_regex:
        email = email_regex.group(1)
    else:
        email = None
    return email

def get_phone(row):
    """takes row of ad_parse as entry, returns phone found in description"""
    phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",row.description)
    if phone_regex:
        phone = phone_regex.group(1)
    else:
        phone = None
    return phone

def get_website(row):
    """takes row of ad_parse as entry, returns website found in description"""
    website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))", row.description)
    if website_regex:
        website = website_regex.group(1)
    else:
        website = None
    return website

def entry_vendor(row, email,phone,website, status_parrot):
    """makes entry into table vendor_analyse, returns nothing"""
    print('make vendor entry') #status in command line
    entry = Vendor_analyse(pseudo=row.pseudo, contact_information=row.contact_information, name=row.name,
                           company=row.company, zip=row.zip, city=row.city, state=row.state, country=row.country,
                           county=row.county, region=row.region, province=row.province,
                           email=row.email, email_description=email, phone=row.phone, phone_description=phone,
                           redirect_website=row.redirect_website, website_deviate=website,
                           status_parrot=status_parrot)  # tous les column sauf id
    entry.insertVendor_analyse(session)
    session.commit()

def get_montant(row):
    """Function which takes row of ad_parse in entry, searches the price and to re"""
    if row.price != None:  # if there is an entry for price
        str_price = str(row.price) #transform to string
        lower_price = str_price.lower() #transform to lowercase
        montant = re.findall(r"(\d+((,\d+)+)?(.\d+)?(.\d+)?(,\d+)?)", lower_price) #regex to find digits (0-9) and get them out
        try:
            montant = montant[0] #if it's in list(tuple)format take out tuple
        except:
            montant = None
        montant_f = None #default
        if montant != None: #if there wasn't an error previously
            list1 = [] #temporary list used for appending the interesting parts in the montant tuple
            for i in montant:
                if i != '' and i != '.00' and i != '.000': #filter out empty info
                    list1.append(i)
            if len(list1) > 1: #if we have more than 1 interesting entry our goal is to calculate a mean
                if '-' in list1[1]: #Case 1: lower-upper price such as 600-800 in the list it will be shown as 600-800 and -800 thus we check second element
                    entrees = list1[0].split('-') #split the first element
                    moyenne = 0
                    flag = False #will be set to true if exception occurs, assures we won't take mean if we only added one element to the list
                    for i in entrees:
                        try:
                            moyenne += int(i)
                        except:
                            flag = True
                    if flag:
                        montant_f = moyenne
                    else:
                        montant_f = moyenne / 2
                if '.' in list1[1]: #case 2: valeurs decimals
                # Imprecision introduit avec ce code:
                # il est presumée que le . denomine centimes si apres point il y a <3 nombres
                    split = list1[0].split('.')
                    if len(split[1]) > 2:
                        try:
                            if len(split) == 2:
                                montant_f = float(''.join(split))
                            else:
                                pass
                        except:
                            pass
                    else:
                        if len(split) == 2:  # only to entrys in split
                            if float(split[0]) != 0:
                                montant_f = float(split[0]) + 1  # prices are rounded up
                            else:
                                montant_f = 0.0
                if ',' in list1[1]: #case 3: decimes
                # Imprecision introduit avec ce code:
                # il est presumée que le , denomine centimes si apres point il y a <3 nombres
                    split = list1[0].split(',')
                    if len(split[1]) > 2:
                        try:
                            if len(split) == 2:
                                montant_f = float(''.join(split))
                            else:
                                pass
                        except:
                            pass
                    else:
                        if len(split) == 2:  # only to entrys in split
                            if float(split[0]) != 0:
                                montant_f = float(split[0]) + 1  # prices are rounded up
                            else:
                                montant_f = 0.0
            else:
                montant_f = float(list1[0])
        return montant_f
    else:
        return None

def transform_currency(row, montant_f):
    """will take the final calculated value as input and return it in the currency of interest"""
    price_final_f = None
    res_currency = None
    if row.price != None:
        price = str(row.price).lower()
        for x in currency_regex: #for each element in the list of our currencies
            if x in price: #look if the currency is found in the price
                res_currency = x #set currency
            # transformer les différentes monnaie
                y = currency_regex.index(res_currency) #get the transforming value
                try:
                    price_final_f = float(montant_f) * float(transform_to_dollar[y]) #transform value
                except:
                    price_final_f = montant_f #if error occurs; do nothing
    return price_final_f, res_currency

def entry_ad_clean(row, id_vendor, price, currency, price_in_dollar):
    """function to make an entry into ads_clean table"""
    entry = Ads_clean(ad_id = row.ad_id, ad_number = row.ad_number, id_vendor=id_vendor, title = row.title,\
    description = row.description, breed = row.breed, age = row.age, sex = row.sex, primary_color = row.primary_color,\
    secondary_color = row.secondary_color, price = price, currency = currency, price_in_dollar= price_in_dollar,payment_forms = row.payment_forms)
    entry.insertAds_clean(session)
    session.commit()

if __name__ == '__main__':
    for row in session.query(Parse_ads):
        #get status_parrot of the ad
        status_parrot = session.query(Classification_3_Ads.parrot).filter_by(ad_id=row.ad_id).scalar() #checks if the ad is classified as parrot
        # get email, website, phone of the ad
        if row.description != None: #if there is a description
            email = get_email(row)
            website = get_website(row)
            phone = get_phone(row)
        else: #else put it to None
            email = None
            website = None
            phone = None
        #create vendor entry if there isn't one
        if session.query(Vendor_analyse).filter_by(pseudo = row.pseudo).scalar()== None: #if there isn't an entry for this pseudo there
            entry_vendor(row, email, phone, website, status_parrot)
        elif session.query(Vendor_analyse.status_parrot).filter_by(pseudo = row.pseudo).scalar == 0: #if there is an entry but the status_parrot is none
            if status_parrot == 1: #but we detect a bird, update
                Vendor_analyse.update(session, 1)
                session.commit()
        #get to creating ads_clean
        montant = get_montant(row)
        real_montant, currency = transform_currency(row, montant)
        vendor_id = session.query(Vendor_analyse.id).filter_by(pseudo=row.pseudo).scalar()
        if montant != None:
            if session.query(Ads_clean.id).filter_by(ad_id=row.ad_id).scalar()==None:
                entry_ad_clean(row, vendor_id, montant, currency, real_montant)
        else:
            if session.query(Ads_clean.id).filter_by(ad_id=row.ad_id).scalar() == None:
                entry_ad_clean(row, vendor_id, montant, None, None)