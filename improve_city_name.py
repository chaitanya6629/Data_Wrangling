import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

def correct_case(name):
    # This function is used to correct the case of city names
    if (name.isupper()):
        bettername = name.title()
        # convert UPPER case names to CAMEL case
    elif (name.islower()):
        bettername = name.title()
        # convert LOWER case names to CAMEL case
    else:
        bettername = name
    
    return bettername

def truncate_extension(name):
    # This function will return the name, truncating the part of the name after ',' or '#'
    # The objective of this function is to remove extensions of city/street names (like 'Tx' or 'Texas') and 
    # any house numbers or suite numbers following city/street names
    if (',' in name):
        bettername = name[:name.index(',')]
        # return the part of the name before ','
    elif ('#' in name):
        bettername = name[:name.index('#')]
        # return the part of the name before '#'
    else:
        bettername = name
    return bettername

def update_city_name(name):
    # This function is used to correct a few spellings in city names and to maintain consistency in city names
    mapping = {
    "Laks Jackson": "Lake Jackson", "Houson": "Houston", "Galveston Island": "Galveston", "The Woodlands": "Woodlands",\
    "Sugarland": "Sugar Land", "West University": "West University Place", "Dickenson": "Dickinson"}
    bettername = correct_case(name)
    bettername1 = truncate_extension(bettername)
    
    if (bettername1 in mapping.keys()):
        bettername2 = mapping[bettername1]
    else:
        bettername2 = bettername1
    return bettername2
    

def improve_city_names():
    
    for city, times in incorrect_city_names.iteritems():
        better_name = update_city_name(city)
        print city, "=>", better_name

improve_city_names()