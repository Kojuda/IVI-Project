"""
Ce script a servi à corriger la table des urls de la base de données pour rajouter un identifiant unique car
le numéro de l'annonce s'est révélé être unique uniquement pour un répertoire de la plateforme concernant un pays.
"""

import  json
from sqlalchemy.sql import exists
from ressources.documentation import Documentation # fichier documentation.py qui se trouve dans le dossier ressource
from ressources.db import *
from ressources.project_utils import get_abr_country

def copy_Ads_Codes() :
    """Function used to copy the ancient table to the new one with 
    the new field ad_id. The object "tmp" does not exist anymore in the
    db.py ressource."""
    for i in session.query(Ads_Codes):
        if session.query(exists().where(Ads_Codes_tmp.ad_number == i.ad_number)).scalar():
            pass
        else :
            with open(f"./results/getCodes/documentation/{i.ad_number}__documentation.json", "r") as f:
                doc = json.loads(f.read())
                url = doc["info"]["selenium"][0]["request"]["url"]
                abr_country=get_abr_country(url)
            entry=Ads_Codes_tmp(
                ad_id=f"{i.ad_number}_{abr_country}",
                ad_number=i.ad_number, 
                client_code = i.client_code,  
                date_created = i.date_created, 
                date_updated = i.date_updated,
                status = i.status,
                status_image_taken = i.status_image_taken,
                status_vendeur_taken = i.status_vendeur_taken)
            entry.insertCode(session)


def copy_Urls_Ads() :
    """Function used to copy the ancient table to the new one with 
    the new field ad_id. The object "tmp" does not exist anymore in the
    db.py ressource."""
    for i in session.query(Urls_ads):
        # if session.query(exists().where(Urls_ads_tmp.ad_number == i.ad_number)).scalar():
        #     pass
        # else :
        abr_country=get_abr_country(i.url)
        entry=Urls_ads_tmp(
            ad_id=f"{i.ad_number}_{abr_country}",
            ad_number=i.ad_number, 
            url = i.url,  
            date_created = i.date_created, 
            date_updated = i.date_updated,
            status = i.status,
            country_id=i.country_id)
        entry.insertURL(session)




if __name__ == "__main__" :
    #copy_Ads_Codes()
    copy_Urls_Ads()