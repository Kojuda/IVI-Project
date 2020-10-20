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

pages = 29
counter = 30
back_pages = counter%pages if pages!=counter else pages
print(back_pages)






# a=Country(name="Suisse", url="test")
# session.add(a)
# session.commit()