from ressources.db import *
import os
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

for row in session.query(Country).all():
    print(row.url)









# a=Country(name="Suisse", url="test")
# session.add(a)
# session.commit()