import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


mapping = { "St": "Street", "St.": "Street", "street": "Street", "Ave": "Avenue", "Rd.": 'Road', "Rd": "Road",\
           "Blvd": "Boulevard", "Blvd.": "Boulevard", "Dr": "Drive", "Fwy": "Freeway", "Frwy": "Freeway", "Hwy": "Highway",\
           "N": "North", "N.": "North", "W": "West", "W.": "West", "E": "East", "E.": "East", "S": "South", "S.": "South",\
           "N ": "North ", "W ": "West ", "E ": "East ", "S ": "South ", "Ln": "Lane", "Farm-to-Market Road 1774": "FM 1774",\
          "Pkwy": "Parkway", "W. ": "West ", "Stree": "Street"}
street_type_re = re.compile(r'\b\S+\.?\s?$', re.IGNORECASE)
    # regex to pull out the street type from the name

def truncate_extension(name):
    # This function will return the name, truncating the part of the name after ',' or '#' or '('
    # The objective of this function is to remove extensions of city/street names (like 'Tx' or 'Texas') and 
    # any house numbers or suite numbers following city/street names
    bettername = name
    match1 = re.compile(r',')
    for m in match1.finditer(name):
        bettername = name[:m.start()]
        # return the part of the name before ','
    match2 = re.compile(r'#')
    for m in match2.finditer(name):
        bettername = name[:m.start()]
        # return the part of the name before '#'

    return bettername


def update_street_name(name):
    mapping = { "St": "Street", "St.": "Street", "street": "Street", "Ave": "Avenue", "Rd.": 'Road', "Rd": "Road",\
           "Blvd": "Boulevard", "Blvd.": "Boulevard", "Dr": "Drive", "Fwy": "Freeway", "Frwy": "Freeway", "Hwy": "Highway",\
           "N": "North", "N.": "North", "W": "West", "W.": "West", "E": "East", "E.": "East", "S": "South", "S.": "South",\
           "N ": "North ", "W ": "West ", "E ": "East ", "S ": "South ", "Ln": "Lane", "Farm-to-Market Road 1774": "FM 1774",\
          "Pkwy": "Parkway", "W. ": "West ", "Stree": "Street"}
    
    better_name = truncate_extension(name)
    
    if ("FM" not in name and name.isupper()):
        better_name = name.title()
        # convert UPPER case names to CAMEL case
        # ignore the street names which have "FM" (Farm to Market Road) in them
    
    if ("Farm-to-Market Road" in name):
        better_name = name.replace("Farm-to-Market Road", "FM")
        # replace "Farm-to-Market Road" with "FM" to maintain consistency
    
    m = street_type_re.search(name)
    if m:
        st_type = m.group()
        if (st_type in mapping.keys()):
            better_name = re.sub(st_type, mapping[st_type], name)
    
    street_abbrev_re = re.compile(r'^([a-z]){1}\.?(\s)+', re.IGNORECASE)
    # regex to pull out abbreviations like E/W/N/S in the name
    m2 = street_abbrev_re.search(better_name)
    better_name2 = better_name
    if m2:
        abbr_name = m2.group()
        if (abbr_name in mapping.keys()):
            better_name2 = re.sub(abbr_name, mapping[m2.group()], better_name)
    
    return better_name2


def improve_street_names():
    for st_type, ways in incorrect_street_types.iteritems():
        for name in ways:
            better_name = update_street_name(name)
            #better_name2 = update_street_name(better_name1)
            print name, "=>", better_name

improve_street_names()