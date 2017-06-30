import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

OSM_FILE = "houston_texas.osm"

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
