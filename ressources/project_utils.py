import re




mapping_countries= {
    "us" : "UNITED STATES",
    "ca" : "CANADA",
    "uk" : "UNITED KINGDOM",
    "ie" : "IRELAND",
    "au" : "AUSTRALIA",
    "nz" : "NEW ZEALAND",
    "sg" : "SINGAPORE",
    "my" : "MALAYSIA",
    "ph" : "PHILIPPINES",
    "id" : "INDONESIA",
    "in" : "INDIA",
    "hk" : "HONG KONG"
}

def map_country(url) :
    abr = re.findall(".*www.adpost.com/(.*?)/.*", url)[0]  #.groups()[0]
    country=mapping_countries[abr]
    return country

def get_abr_country(url) :
    abr = re.findall(".*www.adpost.com/(.*?)/.*", url)[0]
    return abr