from ressources.db import *
from sqlalchemy import and_, exists
import os
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

for row in session.query(Country).all():
    print(row.url)


stmt = session.query(exists().where(and_(Urls_ads.ad_number=="42342", Urls_ads.country_id=="LoL"))).scalar()
print(stmt)








# a=Country(name="Suisse", url="test")
# session.add(a)
# session.commit()