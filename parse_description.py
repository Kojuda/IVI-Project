from ressources.db import session, Parse_ads, Vendor_analyse, Ads_clean
import re
import pdb
currency_regex=["$","£","h","k","rm","php","p","rs","hd","hkd"]
#list_term_regex= [r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))"]
for row in session.query(Parse_ads):
    if row.description != None:
        email_regex =re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",row.description)
        if email_regex:
            email = email_regex.group(1)
            #print(email)
        #import pdb; pdb.set_trace()

        phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",row.description)
        if phone_regex:
            phone = phone_regex.group(1)
            #print (phone)

        website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))",row.description)
        if website_regex:
            website = website_regex.group(1)
            #print (website)





#entree Vendor; avant de faire tester si il y a un antrée deja
    counter_none_pseudo = 0
    if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(Parsing_Psittaciformes_or_no.ad_id == row.ad_id).scalar() != None:
        status_psitasiforme = 1
    else:
        status_psitasiforme = 0
    if row.pseudo!=None:
        if session.query(Vendor_analyse.pseudo).filter_by(pseudo=row.pseudo).scalar()==None:
                entry = Vendor_analyse(pseudo=row.pseudo, contact_information=row.contact_information, name = row.name,company = row.company, zip = row.zip, city = row.city, state = row.state, country = row.country, county = row.county, region= row.region, province = row.province, \
                email = row.email, email_description = email, phone = row.phone, phone_description = phone, redirect_website = row.redirect_website, website_deviate= website, status_psitasiforme = status_psitasiforme)  #tous les column sauf id
                entry.insertVendor_analyse(session)
                session.commit()

    else:
        counter_none_pseudo +=1
        entry = Vendor_analyse(pseudo='withoutpseudo'+str(counter_none_pseudo), contact_information=row.contact_information, name = row.name,company = row.company, zip = row.zip, city = row.city, state = row.state, country = row.country, county = row.county, region= row.region, province = row.province, \
        email = row.email, email_description = email, phone = row.phone, phone_description = phone, redirect_website = row.redirect_website, website_deviate= website)  #tous les column sauf id
        entry.insertVendor_analyse(session)
        session.commit()
