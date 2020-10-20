from ressources.db import *
from sqlalchemy import and_, exists
import os
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

# for row in session.query(Country).all():
#     print(row.url)


stmt = session.query(Urls_ads).filter(Urls_ads.country_id==country).all()
print(stmt)








# a=Country(name="Suisse", url="test")
# session.add(a)
# session.commit()