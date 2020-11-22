from ressources.db import *
from ressources.webdriver import *
from sqlalchemy import and_, exists
import re
import os
from math import floor
from ressources.regex_tools import mp_mit
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











# test = "Amazone à couronne lilas; Lilac-crowned Amazon; Lilac-crowned Parrot; Amazona guayabera; Amazona Guayabera; Cotorra Frente Roja; Loro Corona-violeta;"

# cns = [_.strip(" ") for _ in test.split(";") if (len(_.strip(" "))>0)]
# #List of list of termes included in common names without little words
# cns_decomposed=[[ str.lower(_) for _ in first.split(" ") if (len(_)>2)]  for first in cns if (len(first)>0)]
# #Replace each letter with its mitigation in the mitigation dic
# miss_cns=map(lambda list_words : ("".join([mp_mit[char] if (char in mp_mit.keys())  else char for char in list(word)]) for word in list_words), cns_decomposed)
# #Interpret map object
# miss_cns=[list(_) for _ in list(miss_cns)]
# dict_regex = {}
# #Populate the dict with regex according to each name
# for name_decomposed, name in zip(miss_cns, cns) :
#         reg="".join([f"(?=.*{word})" for word in name])
#         reg=f"^{reg}.*"
#         dict_regex[name]=reg





# regex='^(?=.*[a]{1,2}[f]{1,2}[r]{1,2}[i]{1,2}[c]{1,2}[a]{1,2}[n]{1,2})(?=.*[g]{1,2}[r]{1,2}[e]{1,2}[y]{1,2})(?=.*[p]{1,2}[a]{1,2}[r]{1,2}[r]{1,2}[o]{1,2}[t]{1,2}).*'
# text="""\n\t\t  \tpurebred african grey parrot's available now.,l male and female african grey parrots for sale.parrots are currently being nurtured in a beautiful environment and ready to be shipped worldwide. all our babies are very friendly, entertaining, love been held cuddled and played with and very well socialized. a $280 deposit will reserve the pair for a period of 1 month. all our parrots come with a health certificate from an avian vet and all babies are also disease-free they are vaccinated, checked and tamed, they will come alongside with all bird accessories..... just contact.... for more details about our birds..(magareteambang01@gmail.com)"""

# cp_re=re.compile(regex)
# result=cp_re.search(text, re.DOTALL)
# print(result)

# test="Yellow-headed Amazon"
# s=re.split(" |-", test)
# print(s)



test = "Amazone à couronne lilas; Lilac-crowned Amazon; Lilac-crowned Parrot; Amazona guayabera; Amazona Guayabera; Cotorra Frente Roja; Loro Corona-violeta;"

scientific="Pyrrhura cruentata"
cns = [_.strip(" ") for _ in test.split(";") if (len(_.strip(" "))>0)]
abss = cns.append(scientific.split(" "))
print(cns)