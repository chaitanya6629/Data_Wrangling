import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSM_FILE = "houston_texas.osm"

# This file audits all the fields (street, city, housenumber, postcode, state). 
# Then, it stores all the incorrect/invalid entries in respective lists/dictionaries, which will be used by the cleaning functions.

incorrect_street_types = defaultdict(set) 
# This is a dictionary of street types which contain the street values 
# that are not in the expected list
    
incorrect_state_types = []
# This is a list that contains values of states other than 'TX'
    
incorrect_postcodes = []
# This list contains values of postcodes that are not in Houston or are invalid
    
incorrect_House_Numbers = []
# This list contains values of house numbers that are invalid
    
incorrect_city_names = defaultdict(int)
# This dictionary contains all the invalid city names

# Below are helper functions to audit the fields

def is_street_name(elem):
    return ((elem.tag == "tag") and (elem.attrib['k'] == "addr:street"))

def is_state(elem):
    return ((elem.tag == "tag") and (elem.attrib['k'] == "addr:state" or elem.attrib['k'] == "is_in:state_code"))

def is_postcode(elem):
    return ((elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode"))

def is_housenumber(elem):
    return ((elem.tag == "tag") and (elem.attrib['k'] == "addr:housenumber"))

def is_city(elem):
    return ((elem.tag == "tag") and (elem.attrib['k'] == 'addr:city'))
	
def audit_street_type(street_types, street_name):
    street_type_re = re.compile(r'\b\S+\.?\s?$', re.IGNORECASE)
    expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",\
                "Trail", "Parkway", "Commons", "East", "West", "North", "South", "Freeway", "Highway", "Circle", "Park"]
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_state_type(state_types, state):
    if (state != 'TX'):
        state_types.append(state)

def audit_postcode(incorrect_postcodes, postcode):
    postcode_re = re.compile(r'^(77...)') # Postcode outside Houston, TX
    m = postcode_re.search(postcode)
    if not m:
        incorrect_postcodes.append(postcode)
    return incorrect_postcodes
	
def audit_housenumber(house_numbers, number):
    house_number_re = re.compile(r'^\d+(-?\d)*$')
    m = house_number_re.search(number)
    if not m:
        house_numbers.append(number)
    return house_numbers
	
def audit_city(invalid_city_names, city_name):
    expected = ["Alvin", "Angleton", "Atascocita", "Bay City", "Baytown", "Bellaire", "Brazoria", "Channelview", "Clear Lake Shores", 
            "Clute", "Conroe", "Crosby", "Cypress", "Deer Park", "Dickinson", "Freeport", "Fresno'", "Friendswood", 
            "Galveston", "Hedwig Village", "Hockley", "Houston", "Humble", "Katy", "Kemah", "Kingwood", "Klein", "La Porte", "LaMarque",
            "Lake Jackson", "League City", "Liberty", "Magnolia", "Meadows Place", "Missouri City", "Nassau Bay", "Needville", 
            "Pasadena", "Pearland", "Porter", "Richmond", "Rosenberg", "Santa Fe", "Seabrook", "Shenandoah", "Spring", "Stafford", 
            "Sugar Land", "Texas City", "The Woodlands", "Tomball", "Webster", "West Columbia", "West University Place", "Winnie"]

    if city_name not in expected:
        invalid_city_names[city_name] +=1
    return invalid_city_names
	


def audit_fields(filename):
    # This function will call the helper functions above
    # and populate the lists and dictionaries with incorrect values of respective fields
    
    osm_file = open(filename, 'r')
    
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(incorrect_street_types, elem.attrib['v'])
        elif is_state(elem):
            audit_state_type(incorrect_state_types, elem.attrib['v'])
        elif is_postcode(elem):
            audit_postcode(incorrect_postcodes, elem.attrib['v'])
        elif is_housenumber(elem):
            audit_housenumber(incorrect_House_Numbers, elem.attrib['v'])
        elif is_city(elem):
            audit_city(incorrect_city_names, elem.attrib['v'])
            
    print "Incorrect Street Types: "        
    pprint.pprint(incorrect_street_types)
    print "Incorrect State: "
    pprint.pprint(incorrect_state_types)
    print "Incorrect PostCode: "
    pprint.pprint(incorrect_postcodes)
    print "Incorrect House Numbers: "
    pprint.pprint(incorrect_House_Numbers)
    print "Incorrect City Names: "
    pprint.pprint(incorrect_city_names)

audit_fields(OSM_FILE)
