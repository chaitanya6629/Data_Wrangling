
# coding: utf-8

# # Project: Wrangle OpenStreetMap data 
# ## By: Chaitanya Narayanavaram
# In this project, I have used data wrangling techniques to audit, clean and analyze the data of an area from OpenStreetMap.
# 

# ## Area: Houston, Texas
# Data (.osm) available at: https://mapzen.com/data/metro-extracts/metro/houston_texas/

# ## Importing the necessary libraries:

# In[78]:

import xml.etree.cElementTree as ET
from collections import defaultdict
from pymongo import MongoClient
import pprint
import re
import codecs
import json
import os


# ### Source files:

# In[85]:

path = "C:\Chaitanya\Jupyter\Data_Wrangling\Project_DataWrangling"
SAMPLE_FILE = "houston_texas_sample.osm" # shorter version of the original file (66 MB)
# This sample file is declared here, but the file is written below
OSM_FILE = "houston_texas.osm" # This is the original file (656 MB)


# ### Producing a smaller sample (houston_texas_sample.osm) of the original osm file (houston_texas.osm)

# In[84]:

k = 10 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# ### Analyzing the tags in the OSM file:
# Below we can see what tags are present in the OSM file and how many times each tag occurs 

# In[143]:

def analyze_tags(file):
    tag_types = defaultdict(int)
    for event, elem in ET.iterparse(file):
        tag_types[elem.tag] += 1
    return tag_types
analyze_tags(OSM_FILE)


# ### Tag patterns:

# In[144]:

lower = re.compile(r'^([a-z]|_)*$')
#  tags that contain only lowercase letters and are valid
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
# otherwise valid tags with a colon in their names
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
# tags with problematic characters


def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        
        if lower.search(k_value):
            keys["lower"] += 1
        elif lower_colon.search(k_value):
            keys["lower_colon"] += 1
        elif problemchars.search(k_value):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            # other tags that do not fall into the other three categories
        
    return keys


def process_map_tag_type(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

keys = process_map_tag_type(OSM_FILE)
print "Tags Patterns are: "
pprint.pprint(keys)


# ### Analyzing the keys in tags:
# Below we can see what are the keys that occur in tags and how many times each of them occur.

# In[145]:

def tag_keys(filename):
    tag = defaultdict(int)
    for event, elem in ET.iterparse(filename):
        if (elem.tag == 'way'):
            for e in elem.iter("tag"):
                    tag[e.attrib['k']] +=1
                    # adds the unique 'k' value to the tag dictionary and increments the count if encountered again
                
    return tag
tag_keys(OSM_FILE)
            


# ### Below is the function that will audit a particular field in the tags

# In[146]:

def tag_audit(file, field):
    # This function will accept the file and the field that needs to be analyzed as the input
    # This function will return a dictionary with unique entries in the field (as keys) 
    # and the number of times this unique field has occurred (as values)
    tag = defaultdict(int)
    for event, elem in ET.iterparse(file):
        if (elem.tag == 'way'):
            for e in elem.iter("tag"):
                    if (e.attrib['k'] == field):
                        tag[e.attrib['v']] +=1           
    return tag


# ### Analyzing the values of city in tags:
# Below we can see the values for city and how many times each of them occur in the SAMPLE file

# In[147]:

tag_audit(OSM_FILE, "addr:city")


# In the results above we can observe the following:
# * There are a few entries that have 'Tx'/'Texas' following the city name. This has to be corrected (we will only retain the city name)
# * There is one entry 'Galveston Island' which has to be changes to 'Galveston' to maintain consistency.
# * The first entry '77386' seems to be a pincode value which is erroneously present here. This needs to be removed.
# * 'TEXAS CITY' should be changed to 'Texas City' to maintain consistency.
# * 'West University' and 'West University Place' refer to the same area. So, 'West University' should be changed to 'West University Place' to maintain consistency.
# * 'Sugarland' and 'Sugar Land, TX' should be changed to 'Sugar Land' to maintain consistency as they refer to the same place.
# * 'clear lake shores' should be changed to 'Clear Lake Shores' to maintain consistency as they refer to the same place.

# ### Analyzing the values of street names in tags:
# Below we can see the values for street names and how many times each of them occur in the SAMPLE file

# In[148]:

tag_audit(OSM_FILE, 'addr:street')


# In the results above, we can observe the following:
# * Abbreviations in street names like Dr, Blvd, Pkwy, Fwy need to be corrected (Eg: Dr -> Drive, Blvd -> Boulevard)
# * Abbreviations like E,W,N,S need to be cahnged to East, West, North, South respectively
# * All upper and lower case names need to be changed to camel case to maintain consistency
# * Names with Farm-to-Market Road needs to be changed to "FM" to maintain consistency

# ### Analyzing the country values in the tags:
# Below we can see the values for country and how many times each of them occur in the OSM file

# In[93]:

tag_audit(OSM_FILE, 'addr:country')


# As we can see above, all the country names in the tags are correct and consistent. Thus, there is no need to audit this field further.

# ### Analyzing the house numbers in the tags:
# Below we can see the values for house numbers and how many times each of them occur in the SAMPLE file

# In[149]:

tag_audit(OSM_FILE, 'addr:housenumber')


# From the above results, we can observe that some of the house numbers have street names in them. These need to be corrected.
# For eg: "600 jefferson st" -> "600"

# ### Analyzing the postcodes in the tags
# Below we can see the values for postcodes and how many times each of them occur in the SAMPLE file

# In[97]:

tag_audit(OSM_FILE, 'addr:postcode')


# From the results above, the following can be observed:
# * 73032 belongs to Dougherty, Oklahoma
# * 74404 belongs to Montana
# * 75057 belongs to Dallas, TX
# * 88581 belongs to El Paso, TX
# 
# Also, the extensions like 'TX' need to be removed from postcode

# ### Analyzing the state names in the tags:
# Below we can see the values for states and how many times each of them occur in the SAMPLE file

# In[150]:

tag_audit(OSM_FILE, 'addr:state')


# As we can see from the results above, all of the values have to be changed to 'TX' (which is the most common) to maintain consistency 

# ## Auditing the fields:

# Below are helper functions to audit the fields analyzed above

# In[151]:

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


# In[152]:

def audit_street_type(street_types, street_name):
    street_type_re = re.compile(r'\b\S+\.?\s?$', re.IGNORECASE)
    expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",                "Trail", "Parkway", "Commons", "East", "West", "North", "South", "Freeway", "Highway", "Circle", "Park"]
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# In[153]:

def audit_state_type(state_types, state):
    if (state != 'TX'):
        state_types.append(state)


# In[154]:

def audit_postcode(incorrect_postcodes, postcode):
    postcode_re = re.compile(r'^(77...)') # Postcode outside Houston, TX
    m = postcode_re.search(postcode)
    if not m:
        incorrect_postcodes.append(postcode)
    return incorrect_postcodes


# In[155]:

def audit_housenumber(house_numbers, number):
    house_number_re = re.compile(r'^\d+(-?\d)*$')
    m = house_number_re.search(number)
    if not m:
        house_numbers.append(number)
    return house_numbers


# In[156]:

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


# In[157]:

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


# ## Improving Data Quality of the Fields

# ### Improving the Data Quality of Street Names:

# In[158]:

mapping = { "St": "Street", "St.": "Street", "street": "Street", "Ave": "Avenue", "Rd.": 'Road', "Rd": "Road",           "Blvd": "Boulevard", "Blvd.": "Boulevard", "Dr": "Drive", "Fwy": "Freeway", "Frwy": "Freeway", "Hwy": "Highway",           "N": "North", "N.": "North", "W": "West", "W.": "West", "E": "East", "E.": "East", "S": "South", "S.": "South",           "N ": "North ", "W ": "West ", "E ": "East ", "S ": "South ", "Ln": "Lane", "Farm-to-Market Road 1774": "FM 1774",          "Pkwy": "Parkway", "W. ": "West ", "Stree": "Street"}
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
    mapping = { "St": "Street", "St.": "Street", "street": "Street", "Ave": "Avenue", "Rd.": 'Road', "Rd": "Road",           "Blvd": "Boulevard", "Blvd.": "Boulevard", "Dr": "Drive", "Fwy": "Freeway", "Frwy": "Freeway", "Hwy": "Highway",           "N": "North", "N.": "North", "W": "West", "W.": "West", "E": "East", "E.": "East", "S": "South", "S.": "South",           "N ": "North ", "W ": "West ", "E ": "East ", "S ": "South ", "Ln": "Lane", "Farm-to-Market Road 1774": "FM 1774",          "Pkwy": "Parkway", "W. ": "West ", "Stree": "Street"}
    
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


# ### Improving the Data Quality of City Names:

# In[159]:

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


# ### Improving the Data Quality of House Numbers:

# In[160]:

house_number_re = re.compile(r'^\d+(-?\d)*$')

def update_house_number(house_number):
    street_re = re.compile(r'[a-z]{3}')
    # This regex checks if street name is present in house number field
    
    m1 = street_re.search(house_number)
    better_number = house_number
    if m1:
        #print m1.group(), "    ", house_number
        split = house_number.split(" ")
        if (split[1] != "Suite"):
            return split[0]
        else:
            better_number = house_number
    if ('Ste' in better_number):
        better_number = better_number.replace('Ste', 'Suite')

    return better_number
    


def improve_house_numbers():
    for house_number in incorrect_House_Numbers:
        better_house_number = update_house_number(house_number)
        print house_number, "=>", better_house_number

improve_house_numbers()


# ### Improving the Data Quality of Pincodes:

# In[161]:

def update_postcode(postcode):
    incorrect_list = ['Weslayan Street', '88581', '75057', '7-', '73032', '74404']
    updated_postcode = postcode
    if ('TX ' in postcode):
        updated_postcode = postcode.replace('TX ', '')
    if ('tx ' in postcode):
        updated_postcode = postcode.replace('tx ', '')
    if (postcode in incorrect_list):
        return None
    return updated_postcode

def improve_postcode():
    for pin in incorrect_postcodes:
        better_postcode = update_postcode(pin)
        print pin, "=>", better_postcode


improve_postcode()


# ### Improving the Data Quality of States:

# In[162]:

def update_state_name(name):
    if (name != 'TX'):
        return 'TX'
    else:
        return name

def improve_state():
    for state in incorrect_state_types:
        better_state_name = update_state_name(state)
        print state, "=>", better_state_name

improve_state()


# ## Shaping Elements:

# In[163]:

import xml.etree.cElementTree as ET
import pprint
import re

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way":   
        node["type"] = element.tag
        node["created"] = {}
        created = {}
        node["pos"] =[ None , None]
        pos = [None,None]
        node["address"] = {}
        address={}
        node_refs = []

        for k in element.attrib:
            # Parent Element
            if (k in CREATED):
                created[k] = element.attrib[k]
            elif (k == 'lat'):
                pos[0] = float(element.attrib[k])
            elif (k == 'lon'):
                pos[1] = float(element.attrib[k])
            elif (k in ['id','visible']):
                node[k] = element.attrib[k]
            node['pos'] = pos
            node['created'] = created
            
        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if (tag.attrib['k'] == "addr:street"):
                    address['street'] = update_street_name(tag.attrib['v'])
                            # This will put the cleaned value of street in the address dictionary
                if (tag.attrib['k'] == "addr:city"):
                    address['city'] = update_city_name(tag.attrib['v'])
                            #print address
                            # This will put the cleaned value of city in the address dictionary
                if (tag.attrib['k'] == "addr:housenumber"):
                    address['housenumber'] = update_house_number(tag.attrib['v'])
                            # This will put the cleaned value of housenumber in the address dictionary
                if (tag.attrib['k'] == "addr:postcode"):
                    address['postcode'] = update_postcode(tag.attrib['v'])
                            # This will put the cleaned value of postcode in the address dictionary
                if (tag.attrib['k'] == "addr:state"):
                    address['state'] = update_state_name(tag.attrib['v'])
                            # This will put the cleaned value of state in the address dictionary
                if (tag.attrib['k'].find("addr") == -1):
                            # If not address
                    node[tag.attrib['k']] = tag.attrib['v']
                    
                    
        for n in element.iter("nd"):
            node_refs.append(n.attrib['ref'])

        if address:
            node['address'] = address
        if node["address"] =={}:
            node.pop("address", None)
            
        if node_refs != []:
            node["node_refs"] = node_refs
        return node
    else:
        return None
    
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

data = {}
data = process_map(OSM_FILE, False)


# In[137]:

for entry in data:
    if "address" in entry:
        print entry["address"]
    


# ## Inserting Cleaned Data into MongoDB

# In[164]:

client = MongoClient('mongodb://localhost:27017/')
db = client.houston


# In[166]:

db.collection_houston.insert(data)


# ## Exploring the Database:

# ### Size of the OSM File:

# In[196]:

print "Size of OSM File: ", (os.path.getsize(OSM_FILE))/(1024*1024), "MB"


# ### Size of the Sample File:

# In[197]:

print "Size of Sample File: ", (os.path.getsize(SAMPLE_FILE))/(1024*1024), "MB"


# ### Number of documents, nodes, ways in the database: 

# In[167]:

print "Number of documents = ", db.collection_houston.find().count()


# In[168]:

print "Number of nodes = ", db.collection_houston.find({"type": "node"}).count()


# In[169]:

print "Number of ways = ", db.collection_houston.find({"type": "way"}).count()


# ### Number of Unique Users: 

# In[170]:

pipeline1 = [{"$group": {"_id": "$created.uid"}}]


# In[171]:

count = 0
for doc in db.collection_houston.aggregate(pipeline1):
    #pprint.pprint(doc)
    count = count+1
print "Number of Unique Users = ", count


# ### Top 10 users with maximum contribution:

# In[172]:

pipeline2 = [{"$group": {"_id": "$created.user", "number_of_contributions": {"$sum": 1}}},
            {"$sort": {"number_of_contributions": -1}},
            {"$limit": 10}]


# In[173]:

for doc in db.collection_houston.aggregate(pipeline2):
    pprint.pprint(doc)


# ###  Top 10 popular cuisines in Houston:

# In[188]:

pipeline3 = [{"$match": {"cuisine": {"$ne": None}}},
    {"$group": {"_id": "$cuisine", "freq": {"$sum": 1}}},
            {"$sort": {"freq": -1}},
            {"$limit": 10}]


# In[189]:

for doc in db.collection_houston.aggregate(pipeline3):
    pprint.pprint(doc)


# ### Top 10 most popular amenities:

# In[190]:

pipeline4 = [{"$match": {"amenity": {"$ne": None}}},
    {"$group": {"_id": "$amenity", "freq": {"$sum": 1}}},
            {"$sort": {"freq": -1}},
            {"$limit": 10}]


# In[191]:

for doc in db.collection_houston.aggregate(pipeline4):
    pprint.pprint(doc)

