from ressources.db import *
from ressources.webdriver import *
from sqlalchemy import and_, exists
import re
import os
from math import floor
os.chdir(os.path.dirname(r"{}".format(str(os.path.abspath(__file__)))))

# for row in session.query(Country).all():
#     print(row.url)


# stmt = session.query(Urls_ads).filter(Urls_ads.country_id==country).all()
# print(stmt)


# browser = Firefox(tor=False, headless=True)
# browser.get("https://www.adpost.com/uk/pets/Birds/")
# a=browser.driver.find_element_by_xpath("//div[@style][contains(text(),\"Number of ads: \")]").text
# print(a)
# b=int(re.findall("Number of ads: (\d*)\. .*", a)[0])
# print(floor(b/30))
test = "Amazone à couronne lilas; Lilac-crowned Amazon; Lilac-crowned Parrot; Amazona guayabera; Amazona Guayabera; Cotorra Frente Roja; Loro Corona-violeta;"

cns = [_.strip(" ") for _ in test.split(";")]
        #List of list of termes included in common names without little words
cns_decomposed=[[ str.lower(_) for _ in first.split(" ") if (len(_)>2)]  for first in cns if (len(first)>0)]
print(cns_decomposed)





# a=Country(name="Suisse", url="test")
# session.add(a)
# session.commit()