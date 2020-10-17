from ressources.db import Country, session
import os
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))
a=Country(name="Suisse", url="test")
session.add(a)
session.commit()