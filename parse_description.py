from ressources.db import session, Parse_ads, Vendor_analyse, Ads_clean, Parsing_Psittaciformes_or_no
import re
import pdb

currency_regex=["$","£","h","k","rm","php","p","rs","hd","hkd","sgd","sd","s$"]
transform_to_dollar =["1","1.33","0.13","0.28","0.24","0.021","0.021","0,014","0,13","0,13","0.74","0.74","0.74"]

#currency_regex=["$","£","h","k","rm","php","p","rs","hd","hkd"]
#list_term_regex= [r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))"]
def get_email(row):
    email_regex =re.search(r"((?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",row.description)
    if email_regex:
        email = email_regex.group(1)
    return email

def get_phone(row):
    phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",row.description)
    if phone_regex:
        phone = phone_regex.group(1)
    return phone

def get_website(row):
    website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))", row.description)
    if website_regex:
        website = website_regex.group(1)
    return website

def entry_vendor(row, pseudo):
    entry = Vendor_analyse(pseudo=pseudo, contact_information=row.contact_information, name=row.name,
                           company=row.company, zip=row.zip, city=row.city, state=row.state, country=row.country,
                           county=row.county, region=row.region, province=row.province, \
                           email=row.email, email_description=email, phone=row.phone, phone_description=phone,
                           redirect_website=row.redirect_website, website_deviate=website,
                           status_psitasiforme=status_psitasiforme)  # tous les column sauf id
    entry.insertVendor_analyse(session)
    session.commit()

def get_vendor_info(row):
    if row.description != None:
        email = get_email(row)
        phone = get_phone(row)
        website = get_website(row)
#entree Vendor; avant de faire tester si il y a un antrée deja
    counter_none_pseudo = 0
    if session.query(Parsing_Psittaciformes_or_no.ad_id).filter_by(Parsing_Psittaciformes_or_no.ad_id == row.ad_id).scalar() != None:
        status_psitasiforme = 1
    else:
        status_psitasiforme = 0
    if row.pseudo!=None:
        if session.query(Vendor_analyse.pseudo).filter_by(pseudo=row.pseudo).scalar()==None:
                entry_vendor(row, row.pseudo)

    else:
        counter_none_pseudo +=1
        entry_vendor(row, "pseudo_unknown_"+str(counter_none_pseudo))

def make_entry(row, res_currency_f, price_final_f):
        # if session.query(ids_matching)
    entry = Ads_clean(ad_id=row.ad_id, ad_number=row.ad_number, title=row.title, description=row.description, breed=row.breed, age=row.age, sex=row.sex, primary_color=row.primary_color, secondary_color=row.secondary_color, price=price_final_f, currency=res_currency_f, payment_forms=row.payment_forms)  # tous les column sauf id
    entry.insertAds_clean(session)
    session.commit()

def get_price(row):
    if row.price != None: #if there is an entry for price
         str_price = str(row.price)
         lower_price= str_price.lower()
         #import pdb; pdb.set_trace()
         r_price = lower_price.replace(",","").replace("k ","000")
         montant = re.findall(r"(\d+((,\d+)+)?(.\d+)?(.\d+)?(,\d+)?)", r_price)
         if len(montant)==2:
             try:
                  #import pdb; pdb.set_trace()
                  somme =0
                  denominateur = len(montant)
                  nominateur = float(montant[0][0]) + float (montant[1][0])
                  #import pdb; pdb.set_trace()
                  price_final = int(nominateur) / int(denominateur)
                  #print (price_final)
             except:
                 pass
         else:
             try:
                 price_final = montant[0][0]
                 #print (price_final)
             except:
                pass
         res_currency = None
         for x in currency_regex:
             if x in r_price:
                 res_currency = x
                 #print (res_currency)
                 # transformer les différentes monnaie
                 y = currency_regex.index(res_currency)
                 price_final_f = float(price_final) * float(transform_to_dollar[y])
                 import pdb; pdb.set_trace()
                 res_currency_f = "$"
                 print (res_currency_f)
                 #import pdb; pdb.set_trace()
                 pass
    if session.query(Ads_clean.ad_number).filter_by(ad_number=row.ad_number).scalar()==None:
        make_entry(row,res_currency_f, price_final_f)

if __name__ == '__main__':
    for row in session.query(Parse_ads):
        get_website(row)
        get_price(row)
