from ressources.db import session, Parse_ads, Vendor_analyse, Ads_clean, Parsing_Psittaciformes_or_no, Parsing_bird_or_no
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
    else:
        email = None
    return email

def get_phone(row):
    phone_regex = re.search(r"(((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7})))",row.description)
    if phone_regex:
        phone = phone_regex.group(1)
    else:
        phone = None
    return phone

def get_website(row):
    website_regex = re.search(r"((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))", row.description)
    if website_regex:
        website = website_regex.group(1)
    else:
        website = None
    return website

def entry_vendor(row, email,phone,website, status_bird):
    print('make vendor entry')
    #res = session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()
    entry = Vendor_analyse(pseudo=row.pseudo, contact_information=row.contact_information, name=row.name,
                           company=row.company, zip=row.zip, city=row.city, state=row.state, country=row.country,
                           county=row.county, region=row.region, province=row.province, \
                           email=row.email, email_description=email, phone=row.phone, phone_description=phone,
                           redirect_website=row.redirect_website, website_deviate=website,
                           status_bird=status_bird)  # tous les column sauf id
    entry.insertVendor_analyse(session)
    session.commit()

def get_montant(row):
    if row.price != None:  # if there is an entry for price
        str_price = str(row.price)
        lower_price = str_price.lower()
        # import pdb; pdb.set_trace()
        #r_price = lower_price.replace(",", "").replace("k ", "000") pas possible car k charché pour currency
        montant = re.findall(r"(\d+((,\d+)+)?(.\d+)?(.\d+)?(,\d+)?)", lower_price)
        try:
            montant = montant[0]
        except:
            montant = None
        montant_f = None
        if montant != None:
            list1 = []
            for i in montant:
                if i != '' and i != '.00' and i != '.000':
                    list1.append(i)
            if len(list1) > 1:
                if '-' in list1[1]:
                    entrees = list1[0].split('-')
                    moyenne = 0
                    flag = False
                    for i in entrees:
                        try:
                            moyenne += int(i)
                        except:
                            flag = True
                    if flag:
                        montant_f = moyenne
                    else:
                        montant_f = moyenne / 2
                # print(montant_f, type(montant_f))
                if '.' in list1[1]:
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
                if ',' in list1[1]:
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
    price_final_f = None
    res_currency = None
    if row.price != None:
        price = str(row.price).lower()
        for x in currency_regex:
            if x in price:
                #print('\n change value', price)
                res_currency = x
            # print (res_currency)
            # transformer les différentes monnaie
                y = currency_regex.index(res_currency)
                try:
                    price_final_f = float(montant_f) * float(transform_to_dollar[y])
                except:
                    #print(montant_f, transform_to_dollar[y])
                    price_final_f = montant_f
                #import pdb;
                #pdb.set_trace()
            #res_currency_f = "$"
            # import pdb; pdb.set_trace()
    return price_final_f, res_currency

def entry_ad_clean(row, id_vendor, price, currency, price_in_dollar):
    entry = Ads_clean(ad_id = row.ad_id, ad_number = row.ad_number, id_vendor=id_vendor, title = row.title,\
    description = row.description, breed = row.breed, age = row.age, sex = row.sex, primary_color = row.primary_color,\
    secondary_color = row.secondary_color, price = price, currency = currency, price_in_dollar= price_in_dollar,payment_forms = row.payment_forms)
    entry.insertAds_clean(session)
    session.commit()

if __name__ == '__main__':
    c=0
    for row in session.query(Parse_ads):
        status_bird = session.query(Parsing_bird_or_no.status_bird).filter_by(ad_id=row.ad_id).scalar()
        #print(status_bird)
        if row.description != None:
            email = get_email(row)
            website = get_website(row)
            phone = get_phone(row)
        else:
            email = None
            website = None
            phone = None
        #print(session.query(Vendor_analyse).filter_by(pseudo = row.pseudo).scalar())
        if session.query(Vendor_analyse).filter_by(pseudo = row.pseudo).scalar()== None:
            entry_vendor(row, email, phone, website, status_bird)
        elif session.query(Vendor_analyse.status_bird).filter_by(pseudo = row.pseudo).scalar == 0:
            if status_bird == 1:
                Vendor_analyse.update(session, 1)
        #print(get_price(row))
        #print(c)
        #get_vendor_info(row)
        montant = get_montant(row)
        real_montant, currency = transform_currency(row, montant)
        #if session.query(Ads_clean).filter_by(ad_id = row.ad_id)!= None:
        vendor_id = session.query(Vendor_analyse.id).filter_by(pseudo=row.pseudo).scalar()
        #print(vendor_id)
        if montant != None:
            #print(montant, real_montant, currency)
            if session.query(Ads_clean.id).filter_by(ad_id=row.ad_id).scalar()==None:
                entry_ad_clean(row, vendor_id, montant, currency, real_montant)
        else:
            entry_ad_clean(row, vendor_id, montant, None, None)









        #print(c, email, website, phone, res_currency, price_final)
        c+=1
